from io import BytesIO

from PIL import Image
from ultralytics import YOLO


class ScannerRestauracao:
    """Analisa imagens de mudas via YOLOv8 Nano para medir crescimento e gerar evidências técnicas."""

    # Compartilhado entre instâncias — carregar o modelo por requisição seria inviável em produção
    _modelo: YOLO | None = None

    @classmethod
    def inicializar(cls, caminho_modelo: str = "yolov8n.pt") -> None:
        """Deve ser chamado uma vez na inicialização da API."""
        if cls._modelo is None:
            cls._modelo = YOLO(caminho_modelo)

    def analisar(self, dados_imagem: bytes) -> dict:
        if self._modelo is None:
            raise RuntimeError("Modelo não inicializado. Chame ScannerRestauracao.inicializar() na startup da API.")

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
