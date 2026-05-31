from io import BytesIO

from PIL import Image

try:
    from ultralytics import YOLO
    _YOLO_DISPONIVEL = True
except ImportError:
    _YOLO_DISPONIVEL = False


class ScannerRestauracao:
    """Analisa imagens de mudas via YOLOv8 Nano para medir crescimento e gerar evidências técnicas."""

    _modelo = None

    @classmethod
    def inicializar(cls, caminho_modelo: str = "yolov8n.pt") -> None:
        """Deve ser chamado uma vez na inicialização da API."""
        if not _YOLO_DISPONIVEL:
            return  # fallback mock ativo; sem ultralytics instalado
        if cls._modelo is None:
            try:
                cls._modelo = YOLO(caminho_modelo)
            except Exception:
                pass  # modelo não disponível; fallback mock ativo

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
    
    
