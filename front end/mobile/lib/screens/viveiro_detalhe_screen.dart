import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ViveiroDetalheScreen extends StatefulWidget {
  final String nome;
  final String cientifico;
  final String imageUrl;

  const ViveiroDetalheScreen({
    super.key,
    required this.nome,
    required this.cientifico,
    required this.imageUrl,
  });

  @override
  State<ViveiroDetalheScreen> createState() => _ViveiroDetalheScreenState();
}

class _ViveiroDetalheScreenState extends State<ViveiroDetalheScreen> {
  bool _confirmado = false;
  final _qtdController = TextEditingController(text: '100');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHero(context),
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 40),
              child: _confirmado ? _buildQRPanel() : _buildInfoPanel(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHero(BuildContext context) {
    return Stack(
      children: [
        Image.network(widget.imageUrl,
            width: double.infinity, height: 260, fit: BoxFit.cover,
            errorBuilder: (_, __, ___) => Container(
                height: 260,
                color: AppColors.cerrado.withOpacity(0.15),
                child: const Center(
                    child: Icon(Icons.eco, color: AppColors.cerrado, size: 64)))),
        Positioned.fill(
          child: DecoratedBox(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Colors.transparent, Colors.white],
                stops: [0.5, 1.0],
              ),
            ),
          ),
        ),
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: GestureDetector(
              onTap: () => Navigator.pop(context),
              child: Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.3),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.chevron_left, color: Colors.white, size: 24),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildInfoPanel() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(widget.nome,
            style: const TextStyle(
                fontSize: 24, fontWeight: FontWeight.w800, color: AppColors.text)),
        const SizedBox(height: 4),
        Text(widget.cientifico,
            style: TextStyle(
                fontSize: 11,
                color: Colors.grey.shade500,
                fontStyle: FontStyle.italic)),
        const SizedBox(height: 16),
        Row(
          children: [
            _tag('Sol Pleno', AppColors.cerrado.withOpacity(0.08), AppColors.cerrado),
            const SizedBox(width: 8),
            _tag('Irrigação Moderada', AppColors.river.withOpacity(0.08), AppColors.river),
          ],
        ),
        const SizedBox(height: 24),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.grey.shade50,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.grey.shade100),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('QUANTIDADE SOLICITADA',
                  style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                      color: Colors.grey.shade500,
                      letterSpacing: 1)),
              const SizedBox(height: 8),
              TextField(
                controller: _qtdController,
                keyboardType: TextInputType.number,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                decoration: InputDecoration(
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide(color: Colors.grey.shade200)),
                  enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide(color: Colors.grey.shade200)),
                  focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: AppColors.cerrado, width: 2)),
                ),
              ),
              const SizedBox(height: 6),
              Align(
                alignment: Alignment.centerRight,
                child: Text('Máx disponível: 1.200',
                    style: TextStyle(fontSize: 10, color: Colors.grey.shade400)),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => setState(() => _confirmado = true),
            style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.cerrado,
                minimumSize: const Size(double.infinity, 52)),
            icon: const Icon(Icons.check_circle_outline),
            label: const Text('Confirmar Reserva'),
          ),
        ),
      ],
    );
  }

  Widget _buildQRPanel() {
    return Column(
      children: [
        const SizedBox(height: 8),
        const Text('Reserva Confirmada!',
            style: TextStyle(
                fontSize: 22, fontWeight: FontWeight.w800, color: AppColors.text)),
        const SizedBox(height: 8),
        Text('Apresente este código no viveiro para retirar suas mudas.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 12, color: Colors.grey.shade500)),
        const SizedBox(height: 28),
        Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(24),
            boxShadow: [
              BoxShadow(color: Colors.black.withOpacity(0.09), blurRadius: 30)
            ],
            border: Border.all(color: Colors.grey.shade100),
          ),
          child: Column(
            children: [
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  border: Border.all(color: AppColors.cerrado, width: 4),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: SizedBox(
                  width: 140,
                  height: 140,
                  child: CustomPaint(painter: _QRPainter()),
                ),
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Text('TK-881-A',
                    style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 3)),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Voltar ao Início',
              style: TextStyle(
                  color: Colors.grey.shade600, fontWeight: FontWeight.w600)),
        ),
      ],
    );
  }

  Widget _tag(String text, Color bg, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(6),
          border: Border.all(color: color.withOpacity(0.2))),
      child: Text(text,
          style: TextStyle(
              fontSize: 10, fontWeight: FontWeight.w700, color: color)),
    );
  }
}

class _QRPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFF285430)
      ..style = PaintingStyle.fill;

    final s = size.width / 7;

    void sq(int col, int row) {
      canvas.drawRRect(
        RRect.fromRectAndRadius(
            Rect.fromLTWH(col * s + 1, row * s + 1, s - 2, s - 2),
            const Radius.circular(1.5)),
        paint,
      );
    }

    // Top-left finder pattern
    for (var r = 0; r < 3; r++) for (var c = 0; c < 3; c++) sq(c, r);
    sq(0, 1); sq(2, 1);

    // Top-right finder pattern
    for (var r = 0; r < 3; r++) for (var c = 4; c < 7; c++) sq(c, r);
    sq(4, 1); sq(6, 1);

    // Bottom-left finder pattern
    for (var r = 4; r < 7; r++) for (var c = 0; c < 3; c++) sq(c, r);
    sq(0, 5); sq(2, 5);

    // Inner centers
    sq(1, 1); sq(5, 1); sq(1, 5);

    // Data dots
    for (final pos in [
      [3, 3], [4, 3], [6, 3], [3, 4], [5, 4], [3, 5], [4, 6], [6, 6], [3, 6]
    ]) { sq(pos[0], pos[1]); }
  }

  @override
  bool shouldRepaint(_) => false;
}
