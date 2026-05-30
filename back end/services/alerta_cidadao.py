import os
from io import BytesIO
from datetime import datetime

import httpx
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ExtratorEXIF:
    """Responsável por extrair metadados de localização e tempo de imagens capturadas pelo app."""

    def __init__(self, dados_imagem: bytes):
        self._imagem = Image.open(BytesIO(dados_imagem))

    def extrair_gps(self) -> dict | None:
        exif = self._imagem._getexif()
        if not exif:
            return None

        dados_gps = {}
        for tag_id, valor in exif.items():
            if TAGS.get(tag_id) == "GPSInfo":
                for chave, val in valor.items():
                    dados_gps[GPSTAGS.get(chave, chave)] = val

        if not dados_gps:
            return None

        return {
            "latitude": self._dms_para_decimal(
                dados_gps["GPSLatitude"], dados_gps["GPSLatitudeRef"]
            ),
            "longitude": self._dms_para_decimal(
                dados_gps["GPSLongitude"], dados_gps["GPSLongitudeRef"]
            ),
        }

    def extrair_data_hora(self) -> str | None:
        exif = self._imagem._getexif()
        if not exif:
            return None
        for tag_id, valor in exif.items():
            if TAGS.get(tag_id) == "DateTimeOriginal":
                return valor
        return None

    @staticmethod
    def _dms_para_decimal(dms: tuple, referencia: str) -> float:
        # EXIF armazena GPS em graus/minutos/segundos — converte pra decimal antes de enviar
        graus, minutos, segundos = dms
        decimal = float(graus) + float(minutos) / 60 + float(segundos) / 3600
        if referencia in ("S", "W"):
            decimal *= -1
        return round(decimal, 7)


class AlertaCidadao:
    """Processa a imagem recebida do app e dispara o webhook para o Corpo de Bombeiros."""

    def __init__(self):
        # URL separada por variável de ambiente para suportar homologação e produção sem alterar código
        self._webhook_url = os.getenv("WEBHOOK_BOMBEIROS_URL", "")

    def processar_e_disparar(self, dados_imagem: bytes) -> dict:
        extrator = ExtratorEXIF(dados_imagem)
        gps = extrator.extrair_gps()

        if not gps:
            return {"sucesso": False, "motivo": "Imagem sem dados GPS — verifique se a localização estava ativa"}

        payload = {
            "tipo": "FOCO_INCENDIO",
            "latitude": gps["latitude"],
            "longitude": gps["longitude"],
            "data_hora_captura": extrator.extrair_data_hora() or datetime.utcnow().isoformat(),
            "fonte": "APP_CIDADAO",
        }

        return self._enviar_webhook(payload)

    def _enviar_webhook(self, payload: dict) -> dict:
        if not self._webhook_url:
            # Sem URL configurada, retorna simulação para não bloquear o desenvolvimento
            return {"sucesso": True, "simulado": True, "payload": payload}

        try:
            resposta = httpx.post(self._webhook_url, json=payload, timeout=5.0)
            resposta.raise_for_status()
            return {"sucesso": True, "status_code": resposta.status_code}
        except httpx.HTTPError as e:
            return {"sucesso": False, "motivo": str(e)}
