import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class ScannerRestauracaoScreen extends StatefulWidget {
  const ScannerRestauracaoScreen({super.key});

  @override
  State<ScannerRestauracaoScreen> createState() =>
      _ScannerRestauracaoScreenState();
}

class _ScannerRestauracaoScreenState extends State<ScannerRestauracaoScreen> {
  XFile? _imagem;
  Uint8List? _imagemBytes;
  bool _analisando = false;
  bool _concluido = false;
  Map<String, dynamic>? _resultado;
  String _especie = 'Parkia platycephala (Fava)';
  String _saude = 'saudavel';
  bool _dropdownOpen = false;

  final _especies = const [
    'Parkia platycephala (Fava)',
    'Handroanthus albus (Ipê)',
    'Myracrodruon urundeuva (Aroeira)',
    'Caryocar brasiliense (Pequi)',
  ];

  Future<void> _capturarFoto() async {
    final foto = await ImagePicker()
        .pickImage(source: ImageSource.camera, imageQuality: 90);
    if (foto == null) return;
    final bytes = await foto.readAsBytes();
    setState(() {
      _imagem = foto;
      _imagemBytes = bytes;
      _concluido = false;
      _resultado = null;
    });
  }

  Future<void> _salvarSincronizar() async {
    if (_imagem == null) {
      _capturarFoto();
      return;
    }
    setState(() => _analisando = true);
    try {
      final res = await ApiService.analisarMuda(_imagem!);
      setState(() {
        _analisando = false;
        _concluido = true;
        _resultado = res;
      });
    } catch (_) {
      setState(() => _analisando = false);
    }
    if (!mounted) return;
    if (_concluido) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('Leitura da muda sincronizada no PRAD!'),
            backgroundColor: AppColors.cerrado),
      );
      await Future.delayed(const Duration(seconds: 2));
      if (mounted) Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          _buildCameraBackground(),
          _buildAROverlay(),
          _buildTopBar(),
          _buildBottomSheet(),
        ],
      ),
    );
  }

  Widget _buildCameraBackground() {
    if (_imagemBytes != null) {
      return Image.memory(_imagemBytes!, fit: BoxFit.cover);
    }
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF0A1F10), Color(0xFF1A3520), Color(0xFF0D1207)],
        ),
      ),
    );
  }

  Widget _buildAROverlay() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 280),
      child: Center(
        child: SizedBox(
          width: 260,
          height: 330,
          child: Stack(
            children: [
              CustomPaint(
                size: const Size(260, 330),
                painter: _DashedBorderPainter(),
              ),
              // Green vertical line
              Positioned(
                left: 129,
                top: 20,
                bottom: 80,
                child: Container(
                  width: 2,
                  decoration: BoxDecoration(
                    color: const Color(0xFF4ADE80),
                    boxShadow: [
                      BoxShadow(
                          color: const Color(0xFF4ADE80).withOpacity(0.6),
                          blurRadius: 10,
                          spreadRadius: 2)
                    ],
                  ),
                ),
              ),
              // A4 reference box
              Positioned(
                right: 12,
                bottom: 12,
                child: Container(
                  width: 52,
                  height: 76,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.white, width: 2),
                    color: Colors.white.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: const Center(
                    child: Text('Ref:\nA4',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 9,
                            fontWeight: FontWeight.w700)),
                  ),
                ),
              ),
              // Height badge
              Positioned(
                left: 140,
                top: 36,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.cerrado,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.white, width: 1),
                  ),
                  child: const Text('1.2m (Est.)',
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.w700)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTopBar() {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            GestureDetector(
              onTap: () => Navigator.pop(context),
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    shape: BoxShape.circle),
                child: const Icon(Icons.close, color: Colors.white, size: 20),
              ),
            ),
            GestureDetector(
              onTap: _capturarFoto,
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.black.withOpacity(0.4),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.satellite_alt, color: Colors.white, size: 12),
                    SizedBox(width: 6),
                    Text('GPS Ativo',
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 11,
                            fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBottomSheet() {
    return Positioned(
      bottom: 0,
      left: 0,
      right: 0,
      child: Container(
        padding: const EdgeInsets.fromLTRB(20, 20, 20, 28),
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
          boxShadow: [BoxShadow(color: Colors.black26, blurRadius: 20)],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Container(
                  width: 44,
                  height: 4,
                  decoration: BoxDecoration(
                      color: Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(2))),
            ),
            const SizedBox(height: 16),
            const Text('Ateste de Sobrevivência',
                style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                    color: AppColors.text)),
            const SizedBox(height: 14),
            // Dropdown espécie
            GestureDetector(
              onTap: () => setState(() => _dropdownOpen = !_dropdownOpen),
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  border: Border.all(color: Colors.grey.shade200),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(_especie,
                          style: const TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: AppColors.text),
                          overflow: TextOverflow.ellipsis),
                    ),
                    Icon(
                        _dropdownOpen
                            ? Icons.keyboard_arrow_up
                            : Icons.keyboard_arrow_down,
                        color: Colors.grey.shade400),
                  ],
                ),
              ),
            ),
            if (_dropdownOpen)
              Container(
                margin: const EdgeInsets.only(top: 4),
                decoration: BoxDecoration(
                  color: Colors.white,
                  border: Border.all(color: Colors.grey.shade100),
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                        color: Colors.black.withOpacity(0.08), blurRadius: 12)
                  ],
                ),
                child: Column(
                  children: _especies
                      .map((e) => GestureDetector(
                            onTap: () => setState(() {
                              _especie = e;
                              _dropdownOpen = false;
                            }),
                            child: Container(
                              width: double.infinity,
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 14, vertical: 12),
                              child: Text(e,
                                  style: TextStyle(
                                      fontSize: 13,
                                      fontWeight: e == _especie
                                          ? FontWeight.w700
                                          : FontWeight.normal,
                                      color: e == _especie
                                          ? AppColors.cerrado
                                          : AppColors.text)),
                            ),
                          ))
                      .toList(),
                ),
              ),
            const SizedBox(height: 12),
            // Health buttons
            Row(
              children: [
                _healthBtn('saudavel', 'Saudável', AppColors.cerrado),
                const SizedBox(width: 8),
                _healthBtn('doente', 'Doente', AppColors.jalapao),
                const SizedBox(width: 8),
                _healthBtn('morta', 'Morta', Colors.grey),
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton.icon(
                onPressed: _analisando
                    ? null
                    : (_imagem == null ? _capturarFoto : _salvarSincronizar),
                style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.cerrado, elevation: 0),
                icon: _analisando
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : Icon(_imagem == null
                        ? Icons.camera_alt
                        : Icons.cloud_upload_outlined),
                label: Text(_analisando
                    ? 'Sincronizando...'
                    : _imagem == null
                        ? 'Capturar Foto'
                        : 'Salvar e Sincronizar'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _healthBtn(String value, String label, Color color) {
    final active = _saude == value;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _saude = value),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: active ? color.withOpacity(0.1) : Colors.white,
            border: Border.all(
                color: active ? color : Colors.grey.shade200,
                width: active ? 2 : 1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(label,
              textAlign: TextAlign.center,
              style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  color: active ? color : Colors.grey.shade400)),
        ),
      ),
    );
  }
}

class _DashedBorderPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFFD4A017).withOpacity(0.85)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    const dashLen = 8.0;
    const gapLen = 5.0;
    final path = Path()
      ..addRRect(RRect.fromRectAndRadius(
          Rect.fromLTWH(0, 0, size.width, size.height),
          const Radius.circular(16)));

    for (final m in path.computeMetrics()) {
      double d = 0;
      bool drawing = true;
      while (d < m.length) {
        final next = d + (drawing ? dashLen : gapLen);
        if (drawing) canvas.drawPath(m.extractPath(d, next.clamp(0, m.length)), paint);
        d = next;
        drawing = !drawing;
      }
    }
  }

  @override
  bool shouldRepaint(_) => false;
}
