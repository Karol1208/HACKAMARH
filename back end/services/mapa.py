from schemas import PontoMapa, PoligonoMapa


class MapaService:
    """Fornece os dados geoespaciais para renderização no Leaflet."""

    def obter_pontos(self) -> list[PontoMapa]:
        # Mock — virá do banco de alertas e posições de drones em tempo real
        return [
            PontoMapa(
                lat=-10.7938, lng=-49.6225,
                tipo="foco_incendio",
                titulo="Alerta Cidadão",
                descricao="Incêndio reportado — integrado ao Corpo de Bombeiros",
            ),
            PontoMapa(
                lat=-9.8833, lng=-48.1333,
                tipo="drone",
                titulo="Drone Solar Ninho #04",
                descricao="Status: Varredura Ativa | Bateria: 85%",
            ),
        ]

    def obter_poligonos(self) -> list[PoligonoMapa]:
        # Mock — polígonos CAR virão do cruzamento com o SICAR
        return [
            PoligonoMapa(
                coordenadas=[
                    [-10.2, -48.4], [-10.2, -48.3],
                    [-10.3, -48.3], [-10.3, -48.4],
                ],
                titulo="Fazenda Esperança (CAR)",
                descricao="Módulo B2B — Restauração ativa",
                status="aprovado",
            ),
        ]
