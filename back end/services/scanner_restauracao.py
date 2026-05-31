import hashlib
import logging
import os
from io import BytesIO
from pathlib import Path

from PIL import Image

try:
    from ultralytics import YOLO
    _YOLO_DISPONIVEL = True
except ImportError:
    _YOLO_DISPONIVEL = False

logger = logging.getLogger(__name__)


class ScannerRestauracao:
    """Analisa imagens de mudas via YOLOv8 Nano para medir crescimento e gerar evidências técnicas."""

    _modelo = None

    @classmethod
    def inicializar(cls, caminho_modelo: str = "yolov8n.pt") -> None:
        """Deve ser chamado uma vez na inicialização da API."""
        if not _YOLO_DISPONIVEL:
            return
        if cls._modelo is None:
            try:
                cls._verificar_integridade(caminho_modelo)
                cls._modelo = YOLO(caminho_modelo)
            except Exception as e:
                logger.warning("Scanner indisponível — fallback mock ativo: %s", e)

    @staticmethod
    def _verificar_integridade(caminho_modelo: str) -> None:
        """Compara SHA-256 do arquivo com YOLO_MODEL_SHA256. Ignorado se env não definida."""
        sha256_esperado = os.getenv("YOLO_MODEL_SHA256", "").strip().lower()
        if not sha256_esperado:
            return  # verificação opcional — defina YOLO_MODEL_SHA256 em produção
        arquivo = Path(caminho_modelo)
        if not arquivo.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {caminho_modelo}")
        sha256_real = hashlib.sha256(arquivo.read_bytes()).hexdigest()
        if sha256_real != sha256_esperado:
            raise RuntimeError(
                f"Integridade do modelo comprometida — hash divergente. "
                f"Esperado: {sha256_esperado[:16]}... Real: {sha256_real[:16]}..."
            )

    def analisar(self, dados_imagem: bytes) -> dict:
        if self._modelo is None:
            # Retorna mock realista para demo sem GPU/modelo
            return {
                "total_mudas_detectadas": 3,
                "deteccoes": [
                    {"largura_px": 112.4, "altura_px": 198.7, "confianca": 0.91, "classe": "muda"},
                    {"largura_px": 98.1,  "altura_px": 175.3, "confianca": 0.87, "classe": "muda"},
                    {"largura_px": 104.6, "altura_px": 183.9, "confianca": 0.79, "classe": "muda"},
                ],
                "apta_para_selo": True,
                "simulado": True,
            }

        imagem = Image.open(BytesIO(dados_imagem))
        resultados = self._modelo(imagem, verbose=False)

        deteccoes = self._extrair_deteccoes(resultados[0])

        return {
            "total_mudas_detectadas": len(deteccoes),
            "deteccoes": deteccoes,
            # Apta para selo apenas se detectou mudas com confiança mínima de 60%
            "apta_para_selo": len(deteccoes) > 0 and all(d["confianca"] >= 0.6 for d in deteccoes),
        }

    def _extrair_deteccoes(self, resultado) -> list[dict]:
        deteccoes = []
        for box in resultado.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            # Dimensões em pixels são proxy de tamanho — medição real exige objeto de referência calibrado em campo
            deteccoes.append({
                "largura_px": round(x2 - x1, 2),
                "altura_px": round(y2 - y1, 2),
                "confianca": round(float(box.conf[0]), 4),
                "classe": resultado.names[int(box.cls[0])],
            })
        return deteccoes
    
    
