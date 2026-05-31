import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';
import 'alerta_cidadao_screen.dart';
import 'scanner_restauracao_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Map<String, dynamic>? _kpis;

  @override
  void initState() {
    super.initState();
    _carregarKPIs();
  }

  void _carregarKPIs() async {
    try {
      final data = await ApiService.kpis();
      if (mounted) setState(() => _kpis = data);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bg,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildHeader(),
              const SizedBox(height: 24),
              if (_kpis != null) ...[
                _buildKPIRow(),
                const SizedBox(height: 24),
              ],
              Text('Módulos',
                  style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                      color: Colors.grey,
                      letterSpacing: 1)),
              const SizedBox(height: 12),
              _buildModuloCard(
                titulo: 'Alerta Cidadão',
                subtitulo: 'Denuncie focos de incêndio\ncom foto georreferenciada',
                icone: Icons.local_fire_department_outlined,
                cor: AppColors.fire,
                tag: 'RN01 — Protege',
                onTap: () => Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const AlertaCidadaoScreen())),
              ),
              const SizedBox(height: 12),
              _buildModuloCard(
                titulo: 'Scanner de Mudas',
                subtitulo: 'Ateste o crescimento anual\ndas mudas do seu PRAD',
                icone: Icons.document_scanner_outlined,
                cor: AppColors.cerrado,
                tag: 'RN04 — B2B / Selo Verde',
                onTap: () => Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const ScannerRestauracaoScreen())),
              ),
              const SizedBox(height: 24),
              _buildInfoCard(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            Container(
              width: 38,
              height: 38,
              decoration: BoxDecoration(
                  color: AppColors.cerrado,
                  borderRadius: BorderRadius.circular(10)),
              child: const Icon(Icons.eco, color: Colors.white, size: 20),
            ),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Canindé',
                    style: TextStyle(
                        fontWeight: FontWeight.w800,
                        fontSize: 16,
                        color: AppColors.cerrado)),
                Text('SEMARH / TO',
                    style: TextStyle(
                        fontSize: 9,
                        letterSpacing: 1.5,
                        color: Colors.grey[500],
                        fontWeight: FontWeight.w700)),
              ],
            ),
          ],
        ),
        IconButton(
          icon: const Icon(Icons.logout_outlined, color: Colors.grey),
          onPressed: () => Navigator.pop(context),
        ),
      ],
    );
  }

  Widget _buildKPIRow() {
    return Row(
      children: [
        _kpiChip(
          '${_formatNum(_kpis!['mudas_atestadas'])}',
          'Mudas Atestadas',
          AppColors.cerrado,
        ),
        const SizedBox(width: 10),
        _kpiChip(
          '${_kpis!['selos_verdes']}',
          'Selos Verdes',
          AppColors.jalapao,
        ),
      ],
    );
  }

  Widget _kpiChip(String valor, String label, Color cor) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 12),
        decoration: BoxDecoration(
          color: cor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: cor.withOpacity(0.2)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(valor,
                style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w800,
                    color: cor)),
            const SizedBox(height: 2),
            Text(label,
                style: TextStyle(
                    fontSize: 10,
                    color: cor.withOpacity(0.8),
                    fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }

  Widget _buildModuloCard({
    required String titulo,
    required String subtitulo,
    required IconData icone,
    required Color cor,
    required String tag,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey.shade200),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.04),
                blurRadius: 8,
                offset: const Offset(0, 2))
          ],
        ),
        child: Row(
          children: [
            Container(
              width: 52,
              height: 52,
              decoration: BoxDecoration(
                color: cor.withOpacity(0.12),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Icon(icone, color: cor, size: 26),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(titulo,
                      style: const TextStyle(
                          fontWeight: FontWeight.w800,
                          fontSize: 15,
                          color: AppColors.text)),
                  const SizedBox(height: 3),
                  Text(subtitulo,
                      style: TextStyle(
                          fontSize: 12, color: Colors.grey[600], height: 1.4)),
                  const SizedBox(height: 8),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: cor.withOpacity(0.08),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(tag,
                        style: TextStyle(
                            fontSize: 9,
                            fontWeight: FontWeight.w700,
                            color: cor,
                            letterSpacing: 0.5)),
                  ),
                ],
              ),
            ),
            Icon(Icons.chevron_right, color: Colors.grey[400]),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.river.withOpacity(0.06),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.river.withOpacity(0.15)),
      ),
      child: Row(
        children: [
          const Icon(Icons.info_outline, color: AppColors.river, size: 18),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              'Dados sincronizados com a Central de Inteligência Canindé — SEMARH/TO',
              style: TextStyle(
                  fontSize: 11,
                  color: AppColors.river.withOpacity(0.9),
                  fontWeight: FontWeight.w500),
            ),
          ),
        ],
      ),
    );
  }

  String _formatNum(dynamic n) {
    final num v = n is int ? n : (n as num);
    if (v >= 1000000) return '${(v / 1000000).toStringAsFixed(1)}M';
    if (v >= 1000) return '${(v / 1000).toStringAsFixed(0)}k';
    return v.toString();
  }
}
