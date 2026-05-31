import 'dart:io';
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
  File? _imagem;
  _Estado _estado = _Estado.aguardando;
  Map<String, dynamic>? _resultado;
  String? _erroMsg;

  Future<void> _capturarFoto() async {
    final picker = ImagePicker();
    final foto = await picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 90,
    );
    if (foto == null) return;
    setState(() {
      _imagem = File(foto.path);
      _estado = _Estado.aguardando;
      _resultado = null;
    });
  }

  Future<void> _analisar() async {
    if (_imagem == null) {
      _capturarFoto();
      return;
    }
    setState(() => _estado = _Estado.analisando);
    try {
      final res = await ApiService.analisarMuda(_imagem!);
      setState(() {
        _estado = _Estado.concluido;
        _resultado = res;
      });
    } catch (e) {
      setState(() {
        _estado = _Estado.erro;
        _erroMsg = 'Não foi possível analisar a imagem.\nVerifique sua conexão.';
      });
    }
  }

  void _resetar() {
    setState(() {
      _imagem = null;
      _estado = _Estado.aguardando;
      _resultado = null;
      _erroMsg = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scanner de Mudas'),
        leading: const BackButton(),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(1),
          child: Divider(height: 1, color: Colors.grey.shade200),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildBannerInfo(),
              const SizedBox(height: 20),
              _buildFotoArea(),
              const SizedBox(height: 16),
              if (_estado == _Estado.concluido && _resultado != null)
                _buildResultado(),
              if (_estado == _Estado.erro) _buildErro(),
              if (_estado != _Estado.concluido) _buildBotao(),
              if (_estado == _Estado.concluido) ...[
                _buildBotaoNovo(),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildBannerInfo() {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.cerrado.withOpacity(0.06),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cerrado.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          const Icon(Icons.eco_outlined, color: AppColors.cerrado, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              'Fotografe suas mudas para atestar o crescimento anual via IA. Os dados geram evidências técnicas para o Selo Verde CarbonTO.',
              style: TextStyle(fontSize: 12, color: Colors.grey[700], height: 1.4),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFotoArea() {
    return GestureDetector(
      onTap: _capturarFoto,
      child: Container(
        height: 220,
        width: double.infinity,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: _imagem != null
                ? AppColors.cerrado.withOpacity(0.3)
                : Colors.grey.shade300,
            width: _imagem != null ? 2 : 1,
          ),
        ),
        clipBehavior: Clip.antiAlias,
        child: _imagem != null
            ? Stack(
                fit: StackFit.expand,
                children: [
                  Image.file(_imagem!, fit: BoxFit.cover),
                  Positioned(
                    top: 8,
                    right: 8,
                    child: GestureDetector(
                      onTap: _capturarFoto,
                      child: Container(
                        padding: const EdgeInsets.all(6),
                        decoration: BoxDecoration(
                          color: Colors.black54,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Icon(Icons.camera_alt,
                            color: Colors.white, size: 18),
                      ),
                    ),
                  ),
                ],
              )
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.document_scanner_outlined,
                      size: 44, color: Colors.grey[400]),
                  const SizedBox(height: 10),
                  Text('Toque para fotografar a muda',
                      style: TextStyle(color: Colors.grey[500], fontSize: 13)),
                  const SizedBox(height: 4),
                  Text('Use boa iluminação e fundo limpo',
                      style: TextStyle(color: Colors.grey[400], fontSize: 11)),
                ],
              ),
      ),
    );
  }

  Widget _buildResultado() {
    final total = _resultado!['total_mudas_detectadas'] as int? ?? 0;
    final apta = _resultado!['apta_para_selo'] as bool? ?? false;
    final deteccoes = (_resultado!['deteccoes'] as List?) ?? [];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.only(bottom: 16),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: apta
                  ? [AppColors.cerrado, const Color(0xFF1B6B35)]
                  : [AppColors.jalapao, const Color(0xFFB8860B)],
            ),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Row(
            children: [
              Icon(
                apta ? Icons.verified : Icons.pending_outlined,
                color: Colors.white,
                size: 32,
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      apta ? 'Apta para Selo Verde!' : 'Análise Inconclusiva',
                      style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w800,
                          fontSize: 15),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      '$total muda${total != 1 ? 's' : ''} detectada${total != 1 ? 's' : ''}',
                      style: const TextStyle(
                          color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        if (deteccoes.isNotEmpty) ...[
          const Text('Detecções por IA',
              style: TextStyle(
                  fontWeight: FontWeight.w700,
                  fontSize: 13,
                  color: AppColors.text)),
          const SizedBox(height: 8),
          ...deteccoes.asMap().entries.map((e) {
            final d = e.value as Map;
            final conf = ((d['confianca'] as num) * 100).toStringAsFixed(0);
            final h = (d['altura_px'] as num).toStringAsFixed(0);
            final w = (d['largura_px'] as num).toStringAsFixed(0);
            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.grey.shade200),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.eco, color: AppColors.cerrado, size: 16),
                      const SizedBox(width: 8),
                      Text('Muda ${e.key + 1}',
                          style: const TextStyle(
                              fontWeight: FontWeight.w600, fontSize: 13)),
                    ],
                  ),
                  Row(
                    children: [
                      _metricaChip('${w}×${h}px', Colors.grey.shade100,
                          Colors.grey.shade600),
                      const SizedBox(width: 6),
                      _metricaChip('$conf%', AppColors.cerrado.withOpacity(0.1),
                          AppColors.cerrado),
                    ],
                  ),
                ],
              ),
            );
          }),
        ],
        const SizedBox(height: 16),
      ],
    );
  }

  Widget _metricaChip(String label, Color bg, Color text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration:
          BoxDecoration(color: bg, borderRadius: BorderRadius.circular(6)),
      child: Text(label,
          style:
              TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: text)),
    );
  }

  Widget _buildErro() {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.fire.withOpacity(0.07),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.fire.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          const Icon(Icons.error_outline, color: AppColors.fire, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Text(_erroMsg ?? '',
                style: const TextStyle(
                    fontSize: 12, color: AppColors.fire, height: 1.4)),
          ),
        ],
      ),
    );
  }

  Widget _buildBotao() {
    final semFoto = _imagem == null;
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: _estado == _Estado.analisando ? null : _analisar,
        icon: _estado == _Estado.analisando
            ? const SizedBox(
                width: 18,
                height: 18,
                child: CircularProgressIndicator(
                    color: Colors.white, strokeWidth: 2))
            : Icon(semFoto ? Icons.camera_alt : Icons.document_scanner),
        label: Text(_estado == _Estado.analisando
            ? 'Analisando com IA...'
            : semFoto
                ? 'Tirar Foto da Muda'
                : 'Analisar com IA'),
      ),
    );
  }

  Widget _buildBotaoNovo() {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: _resetar,
            icon: const Icon(Icons.refresh, color: AppColors.cerrado),
            label: const Text('Nova Análise',
                style: TextStyle(color: AppColors.cerrado)),
            style: OutlinedButton.styleFrom(
              minimumSize: const Size(double.infinity, 52),
              side: const BorderSide(color: AppColors.cerrado),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14)),
            ),
          ),
        ),
      ],
    );
  }
}

enum _Estado { aguardando, analisando, concluido, erro }
