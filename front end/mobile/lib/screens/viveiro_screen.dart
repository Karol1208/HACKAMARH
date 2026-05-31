import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'viveiro_detalhe_screen.dart';

class ViveiroScreen extends StatelessWidget {
  const ViveiroScreen({super.key});

  static const _mudas = [
    {
      'nome': 'Ipê Amarelo',
      'cientifico': 'Handroanthus albus',
      'viveiro': 'Viveiro Palmas',
      'quantidade': '1.200 un. disp.',
      'imagem': 'https://picsum.photos/seed/ipe/200/200',
    },
    {
      'nome': 'Parkia platycephala',
      'cientifico': 'Fava de Bolota',
      'viveiro': 'Viveiro Araguaína',
      'quantidade': '450 un. disp.',
      'imagem': 'https://picsum.photos/seed/fava/200/200',
    },
    {
      'nome': 'Aroeira do Sertão',
      'cientifico': 'Myracrodruon urundeuva',
      'viveiro': 'Viveiro Palmas',
      'quantidade': '780 un. disp.',
      'imagem': 'https://picsum.photos/seed/aroeira/200/200',
    },
    {
      'nome': 'Pequizeiro',
      'cientifico': 'Caryocar brasiliense',
      'viveiro': 'Viveiro Porto Nacional',
      'quantidade': '320 un. disp.',
      'imagem': 'https://picsum.photos/seed/pequi/200/200',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(child: _buildHeader()),
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(20, 20, 20, 20),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                _buildSearch(),
                const SizedBox(height: 16),
                ..._mudas.map((m) => Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _buildCard(context, m),
                    )),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.fromLTRB(24, 52, 24, 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Viveiros Estaduais',
              style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w800,
                  color: AppColors.text)),
          const SizedBox(height: 4),
          Text('Reserva de mudas para recuperação',
              style: TextStyle(fontSize: 12, color: Colors.grey.shade500)),
        ],
      ),
    );
  }

  Widget _buildSearch() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 8)
        ],
      ),
      child: TextField(
        decoration: InputDecoration(
          hintText: 'Buscar por espécie nativa...',
          hintStyle: TextStyle(color: Colors.grey.shade400, fontSize: 13),
          prefixIcon: Icon(Icons.search, color: Colors.grey.shade400, size: 20),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(vertical: 14),
        ),
      ),
    );
  }

  Widget _buildCard(BuildContext context, Map<String, String> m) {
    return GestureDetector(
      onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
              builder: (_) => ViveiroDetalheScreen(
                    nome: m['nome']!,
                    cientifico: m['cientifico']!,
                    imageUrl: m['imagem']!,
                  ))),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey.shade100),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.04),
                blurRadius: 8,
                offset: const Offset(0, 2))
          ],
        ),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.network(m['imagem']!,
                  width: 64, height: 64, fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(
                      width: 64, height: 64,
                      color: AppColors.cerrado.withOpacity(0.1),
                      child: const Icon(Icons.eco, color: AppColors.cerrado))),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(m['nome']!,
                      style: const TextStyle(
                          fontWeight: FontWeight.w700,
                          fontSize: 14,
                          color: AppColors.text)),
                  const SizedBox(height: 3),
                  Text('${m['viveiro']} • ${m['quantidade']}',
                      style: TextStyle(fontSize: 10, color: Colors.grey.shade500)),
                  const SizedBox(height: 8),
                  const Text('Reservar Lote →',
                      style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: AppColors.river)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
