import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'alerta_cidadao_screen.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          Image.network(
            'https://picsum.photos/seed/cerrado/600/900',
            fit: BoxFit.cover,
            color: AppColors.cerrado.withOpacity(0.55),
            colorBlendMode: BlendMode.multiply,
            errorBuilder: (_, __, ___) => Container(color: AppColors.cerrado),
          ),
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [Colors.transparent, Color(0xCC0D1F10), Color(0xEE000000)],
                stops: [0.0, 0.55, 1.0],
              ),
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(24, 20, 24, 24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Spacer(flex: 2),
                  Container(
                    width: 64,
                    height: 64,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(18),
                      border: Border.all(color: Colors.white.withOpacity(0.25)),
                    ),
                    child: const Icon(Icons.eco, color: Colors.white, size: 30),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'Esta terra\né nossa.',
                    style: TextStyle(
                      fontSize: 38,
                      fontWeight: FontWeight.w800,
                      color: Colors.white,
                      height: 1.15,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'PROJETO CANINDÉ',
                    style: TextStyle(
                      color: AppColors.jalapao,
                      fontWeight: FontWeight.w700,
                      fontSize: 11,
                      letterSpacing: 3.5,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Monitoramento ambiental, acesso a mudas e validação de créditos de carbono do Tocantins.',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.75),
                      fontSize: 14,
                      height: 1.65,
                    ),
                  ),
                  const Spacer(flex: 3),
                  _buildBtn(
                    onTap: () => Navigator.pushReplacementNamed(context, '/main'),
                    bgColor: Colors.white,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.river,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Text('gov.br',
                              style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w800)),
                        ),
                        const SizedBox(width: 10),
                        const Text('Acesso Produtor (CAR)',
                            style: TextStyle(color: AppColors.cerrado, fontWeight: FontWeight.w700, fontSize: 15)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildBtn(
                    onTap: () => Navigator.push(
                        context, MaterialPageRoute(builder: (_) => const AlertaCidadaoScreen())),
                    bgColor: AppColors.fire.withOpacity(0.2),
                    borderColor: AppColors.fire.withOpacity(0.5),
                    child: const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.warning_amber_rounded, color: Colors.white, size: 18),
                        SizedBox(width: 8),
                        Text('Denunciar Queimada',
                            style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBtn({
    required VoidCallback onTap,
    required Color bgColor,
    Color? borderColor,
    required Widget child,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: double.infinity,
        height: 56,
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(16),
          border: borderColor != null ? Border.all(color: borderColor) : null,
        ),
        alignment: Alignment.center,
        child: child,
      ),
    );
  }
}
