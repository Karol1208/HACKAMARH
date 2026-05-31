import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:geolocator/geolocator.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class AlertaCidadaoScreen extends StatefulWidget {
  const AlertaCidadaoScreen({super.key});

  @override
  State<AlertaCidadaoScreen> createState() => _AlertaCidadaoScreenState();
}

class _AlertaCidadaoScreenState extends State<AlertaCidadaoScreen> {
  CameraController? _controller;
  bool _cameraReady = false;

  XFile? _imagem;
  Uint8List? _imagemBytes;
  Position? _posicao;
  bool _enviando = false;
  bool _enviado = false;

  @override
  void initState() {
    super.initState();
    _obterLocalizacao();
    _initCamera();
  }

  Future<void> _initCamera() async {
    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) return;
      _controller = CameraController(
        cameras.first,
        ResolutionPreset.high,
        enableAudio: false,
      );
      await _controller!.initialize();
      if (mounted) setState(() => _cameraReady = true);
    } catch (_) {}
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _obterLocalizacao() async {
    try {
      bool ativo = await Geolocator.isLocationServiceEnabled();
      if (!ativo) return;
      LocationPermission perm = await Geolocator.checkPermission();
      if (perm == LocationPermission.denied) {
        perm = await Geolocator.requestPermission();
        if (perm == LocationPermission.denied) return;
      }
      final pos = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high);
      if (mounted) setState(() => _posicao = pos);
    } catch (_) {}
  }

  Future<void> _capturarFoto() async {
    if (_controller == null || !_controller!.value.isInitialized) return;
    try {
      final foto = await _controller!.takePicture();
      final bytes = await foto.readAsBytes();
      setState(() {
        _imagem = foto;
        _imagemBytes = bytes;
      });
    } catch (_) {}
  }

  Future<void> _enviar() async {
    setState(() => _enviando = true);
    try {
      if (_imagem != null) await ApiService.enviarAlertaIncendio(_imagem!);
    } catch (_) {}
    if (!mounted) return;
    setState(() {
      _enviando = false;
      _enviado = true;
    });
    await Future.delayed(const Duration(seconds: 2));
    if (mounted) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          _buildBackground(),
          _buildReticle(),
          _buildTopBar(),
          _buildBottomSheet(),
        ],
      ),
    );
  }

  Widget _buildBackground() {
    if (_imagemBytes != null) {
      return Image.memory(_imagemBytes!, fit: BoxFit.cover);
    }
    if (_cameraReady && _controller != null) {
      return CameraPreview(_controller!);
    }
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF3D0A0A), Color(0xFF7A1A1A), Color(0xFF1A0505)],
        ),
      ),
    );
  }

  Widget _buildReticle() {
    const s = 220.0;
    const c = 26.0;
    const w = 4.0;
    return Center(
      child: SizedBox(
        width: s,
        height: s,
        child: Stack(
          children: [
            Positioned(top: 0, left: 0, child: _corner(top: true, left: true, c: c, w: w)),
            Positioned(top: 0, right: 0, child: _corner(top: true, left: false, c: c, w: w)),
            Positioned(bottom: 0, left: 0, child: _corner(top: false, left: true, c: c, w: w)),
            Positioned(bottom: 0, right: 0, child: _corner(top: false, left: false, c: c, w: w)),
            Center(child: Icon(Icons.local_fire_department_outlined,
                color: Colors.white.withOpacity(0.4), size: 52)),
          ],
        ),
      ),
    );
  }

  Widget _corner({required bool top, required bool left, required double c, required double w}) {
    return Container(
      width: c,
      height: c,
      decoration: BoxDecoration(
        border: Border(
          top: top ? BorderSide(color: Colors.white, width: w) : BorderSide.none,
          bottom: !top ? BorderSide(color: Colors.white, width: w) : BorderSide.none,
          left: left ? BorderSide(color: Colors.white, width: w) : BorderSide.none,
          right: !left ? BorderSide(color: Colors.white, width: w) : BorderSide.none,
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
                    color: Colors.white.withOpacity(0.2), shape: BoxShape.circle),
                child: const Icon(Icons.chevron_left, color: Colors.white, size: 24),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: AppColors.fire,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(color: AppColors.fire.withOpacity(0.5), blurRadius: 12)
                ],
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                      width: 6,
                      height: 6,
                      decoration: const BoxDecoration(
                          color: Colors.white, shape: BoxShape.circle)),
                  const SizedBox(width: 6),
                  const Text('Protege CBM-TO',
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.w700)),
                ],
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
          boxShadow: [BoxShadow(color: Colors.black38, blurRadius: 24)],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey.shade50,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade100),
              ),
              child: Row(
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    decoration: BoxDecoration(
                        color: AppColors.fire.withOpacity(0.1),
                        shape: BoxShape.circle),
                    child: const Icon(Icons.location_on, color: AppColors.fire, size: 16),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('LOCALIZAÇÃO EXIF (AUTOMÁTICA)',
                            style: TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.w700,
                                color: Colors.grey.shade500,
                                letterSpacing: 0.5)),
                        const SizedBox(height: 2),
                        Text(
                          _posicao != null
                              ? '${_posicao!.latitude.toStringAsFixed(4)}, ${_posicao!.longitude.toStringAsFixed(4)}'
                              : '-10.1833, -48.3333',
                          style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w700,
                              fontFamily: 'monospace'),
                        ),
                      ],
                    ),
                  ),
                  GestureDetector(
                    onTap: _capturarFoto,
                    child: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                          color: AppColors.river.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8)),
                      child: const Icon(Icons.camera_alt_outlined,
                          color: AppColors.river, size: 16),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: (_enviando || _enviado) ? null : _enviar,
                style: ElevatedButton.styleFrom(
                  backgroundColor: _enviado ? AppColors.cerrado : AppColors.fire,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14)),
                  elevation: 0,
                ),
                child: _enviando
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            color: Colors.white, strokeWidth: 2))
                    : _enviado
                        ? const Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.check_circle, color: Colors.white, size: 18),
                              SizedBox(width: 8),
                              Text('Alerta Recebido pelos Bombeiros!',
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w700,
                                      fontSize: 13)),
                            ],
                          )
                        : Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Container(
                                width: 22,
                                height: 22,
                                decoration: BoxDecoration(
                                    border: Border.all(
                                        color: Colors.white, width: 2),
                                    shape: BoxShape.circle),
                                child: Center(
                                    child: Container(
                                        width: 8,
                                        height: 8,
                                        decoration: const BoxDecoration(
                                            color: Colors.white,
                                            shape: BoxShape.circle))),
                              ),
                              const SizedBox(width: 10),
                              const Text('Denunciar Anonimamente',
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w700,
                                      fontSize: 15)),
                            ],
                          ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
