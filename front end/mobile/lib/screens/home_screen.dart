import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';
import 'scanner_restauracao_screen.dart';
import 'alerta_cidadao_screen.dart';

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
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHeader(),
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 20),
              child: Column(
                children: [
                  _buildPRADAlert(),
                  const SizedBox(height: 20),
                  _buildScannerCard(),
                  const SizedBox(height: 16),
                  _buildKPIGrid(),
                  const SizedBox(height: 16),
                  _buildFireAlert(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.fromLTRB(24, 52, 24, 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('CAR: TO-492112...',
                  style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                      color: Colors.grey.shade400,
                      letterSpacing: 1)),
              const SizedBox(height: 2),
              const Text('Fazenda Vale Verde',
                  style: TextStyle(
                      fontSize: 20, fontWeight: FontWeight.w800, color: AppColors.text)),
            ],
          ),
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: AppColors.river.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.logout_outlined, color: AppColors.river, size: 18),
          ),
        ],
      ),
    );
  }

  Widget _buildPRADAlert() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
            colors: [AppColors.jalapao, Color(0xFFF97316)]),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
              color: AppColors.jalapao.withOpacity(0.3),
              blurRadius: 14,
              offset: const Offset(0, 4))
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.calendar_today_outlined, color: Colors.white, size: 22),
          ),
          const SizedBox(width: 14),
          const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Leitura PRAD Exigida',
                  style: TextStyle(
                      color: Colors.white, fontWeight: FontWeight.w700, fontSize: 14)),
              SizedBox(height: 2),
              Text('Prazo encerra em 15 dias.',
                  style: TextStyle(color: Color(0xFFFFF3CD), fontSize: 12)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildScannerCard() {
    return GestureDetector(
      onTap: () => Navigator.push(
          context, MaterialPageRoute(builder: (_) => const ScannerRestauracaoScreen())),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: AppColors.cerrado,
          borderRadius: BorderRadius.circular(24),
          boxShadow: [
            BoxShadow(
                color: AppColors.cerrado.withOpacity(0.3),
                blurRadius: 20,
                offset: const Offset(0, 6))
          ],
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: const EdgeInsets.all(6),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.document_scanner_outlined,
                        color: Colors.white, size: 18),
                  ),
                  const SizedBox(height: 10),
                  const Text('Scanner (Câmera)',
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w700,
                          fontSize: 18)),
                  const SizedBox(height: 4),
                  const Text('Meça a sobrevivência das mudas.',
                      style: TextStyle(color: Color(0xFFBBF7D0), fontSize: 12)),
                  const SizedBox(height: 16),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Text('Iniciar Medição',
                        style: TextStyle(
                            color: AppColors.cerrado,
                            fontWeight: FontWeight.w700,
                            fontSize: 12)),
                  ),
                ],
              ),
            ),
            const Icon(Icons.camera_alt_outlined, color: Colors.white, size: 56),
          ],
        ),
      ),
    );
  }

  Widget _buildKPIGrid() {
    final mudas = _kpis?['mudas_atestadas'] ?? 1240;
    return Row(
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.grey.shade100),
              boxShadow: [
                BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 8)
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(Icons.eco_outlined, color: AppColors.cerrado, size: 22),
                const SizedBox(height: 12),
                Text(_formatNum(mudas),
                    style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w800,
                        color: AppColors.text)),
                Text('Mudas Vivas',
                    style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w700,
                        color: Colors.grey.shade400)),
              ],
            ),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 8)
                ],
              ),
              child: IntrinsicHeight(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Container(width: 4, color: AppColors.river),
                    const Expanded(
                      child: Padding(
                        padding: EdgeInsets.all(14),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Icon(Icons.verified_outlined, color: AppColors.river, size: 22),
                            SizedBox(height: 12),
                            Text('Selo de Carbono',
                                style: TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.w700,
                                    color: Colors.grey)),
                            SizedBox(height: 4),
                            Text('Elegível 92%',
                                style: TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w700,
                                    color: AppColors.river)),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFireAlert() {
    return GestureDetector(
      onTap: () => Navigator.push(
          context, MaterialPageRoute(builder: (_) => const AlertaCidadaoScreen())),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFFFFF1F1),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: const Color(0xFFFFDEDE)),
        ),
        child: const Row(
          children: [
            Icon(Icons.local_fire_department_outlined, color: AppColors.fire, size: 22),
            SizedBox(width: 12),
            Expanded(
                child: Text('Reportar Queimada',
                    style: TextStyle(
                        color: AppColors.fire,
                        fontWeight: FontWeight.w700,
                        fontSize: 14))),
            Icon(Icons.chevron_right, color: AppColors.fire, size: 18),
          ],
        ),
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
