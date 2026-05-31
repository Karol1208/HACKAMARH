import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class AlertaCidadaoScreen extends StatefulWidget {
  const AlertaCidadaoScreen({super.key});

  @override
  State<AlertaCidadaoScreen> createState() => _AlertaCidadaoScreenState();
}

class _AlertaCidadaoScreenState extends State<AlertaCidadaoScreen> {
  File? _imagem;
  Position? _posicao;
  _Estado _estado = _Estado.aguardando;
  String? _mensagem;
  Map<String, dynamic>? _resultado;

  Future<void> _capturarFoto() async {
    final picker = ImagePicker();
    final foto = await picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 85,
    );
    if (foto == null) return;

    setState(() {
      _imagem = File(foto.path);
      _estado = _Estado.aguardando;
      _resultado = null;
    });

    await _obterLocalizacao();
  }

  Future<void> _obterLocalizacao() async {
    try {
      bool servicoAtivo = await Geolocator.isLocationServiceEnabled();
      if (!servicoAtivo) return;

      LocationPermission permissao = await Geolocator.checkPermission();
      if (permissao == LocationPermission.denied) {
        permissao = await Geolocator.requestPermission();
        if (permissao == LocationPermission.denied) return;
      }

      final pos = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() => _posicao = pos);
    } catch (_) {}
  }

  Future<void> _enviarAlerta() async {
    if (_imagem == null) {
      _capturarFoto();
      return;
    }

    setState(() => _estado = _Estado.enviando);

    try {
      final res = await ApiService.enviarAlertaIncendio(_imagem!);
      setState(() {
        _estado = _Estado.sucesso;
        _resultado = res;
        _mensagem = res['simulado'] == true
            ? 'Alerta registrado (modo dev)\nBombeiros serão notificados em produção.'
            : 'Alerta enviado ao Corpo de Bombeiros!';
      });
    } catch (e) {
      setState(() {
        _estado = _Estado.erro;
        _mensagem = 'Não foi possível enviar o alerta.\nVerifique sua conexão.';
      });
    }
  }

  void _resetar() {
    setState(() {
      _imagem = null;
      _posicao = null;
      _estado = _Estado.aguardando;
      _mensagem = null;
      _resultado = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alerta Cidadão'),
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
              if (_posicao != null) _buildGPSChip(),
              if (_posicao != null) const SizedBox(height: 16),
              if (_estado == _Estado.sucesso) _buildSucesso(),
              if (_estado == _Estado.erro) _buildErro(),
              if (_estado != _Estado.sucesso) _buildBotao(),
              if (_estado == _Estado.sucesso) _buildBotaoNovo(),
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
        color: AppColors.fire.withOpacity(0.06),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.fire.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          const Icon(Icons.local_fire_department, color: AppColors.fire, size: 20),
          const SizedBox(width: 10),
          Expanded(
            child: Text(
              'Tire uma foto do foco de incêndio. O GPS será capturado automaticamente e o alerta enviado ao Corpo de Bombeiros.',
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
              width: _imagem != null ? 2 : 1),
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
                  Icon(Icons.camera_alt_outlined,
                      size: 40, color: Colors.grey[400]),
                  const SizedBox(height: 10),
                  Text('Toque para fotografar o foco',
                      style: TextStyle(color: Colors.grey[500], fontSize: 13)),
                  const SizedBox(height: 4),
                  Text('A câmera será aberta',
                      style: TextStyle(color: Colors.grey[400], fontSize: 11)),
                ],
              ),
      ),
    );
  }

  Widget _buildGPSChip() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.cerrado.withOpacity(0.08),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: AppColors.cerrado.withOpacity(0.2)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.location_on, color: AppColors.cerrado, size: 14),
          const SizedBox(width: 6),
          Text(
            '${_posicao!.latitude.toStringAsFixed(5)}, ${_posicao!.longitude.toStringAsFixed(5)}',
            style: const TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w600,
                color: AppColors.cerrado,
                fontFamily: 'monospace'),
          ),
        ],
      ),
    );
  }

  Widget _buildSucesso() {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.cerrado.withOpacity(0.07),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.cerrado.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          const Icon(Icons.check_circle, color: AppColors.cerrado, size: 22),
          const SizedBox(width: 10),
          Expanded(
            child: Text(_mensagem ?? '',
                style: const TextStyle(
                    fontSize: 13, color: AppColors.cerrado, height: 1.4)),
          ),
        ],
      ),
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
            child: Text(_mensagem ?? '',
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
        onPressed: _estado == _Estado.enviando ? null : _enviarAlerta,
        style: ElevatedButton.styleFrom(
          backgroundColor: semFoto ? AppColors.river : AppColors.fire,
        ),
        icon: _estado == _Estado.enviando
            ? const SizedBox(
                width: 18,
                height: 18,
                child: CircularProgressIndicator(
                    color: Colors.white, strokeWidth: 2))
            : Icon(semFoto ? Icons.camera_alt : Icons.send),
        label: Text(_estado == _Estado.enviando
            ? 'Enviando alerta...'
            : semFoto
                ? 'Tirar Foto'
                : 'Enviar Alerta aos Bombeiros'),
      ),
    );
  }

  Widget _buildBotaoNovo() {
    return SizedBox(
      width: double.infinity,
      child: OutlinedButton.icon(
        onPressed: _resetar,
        icon: const Icon(Icons.refresh, color: AppColors.cerrado),
        label: const Text('Novo Alerta',
            style: TextStyle(color: AppColors.cerrado)),
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(double.infinity, 52),
          side: const BorderSide(color: AppColors.cerrado),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        ),
      ),
    );
  }
}

enum _Estado { aguardando, enviando, sucesso, erro }
