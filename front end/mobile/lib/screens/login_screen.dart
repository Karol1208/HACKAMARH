import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'home_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _credencial = TextEditingController();
  final _senha = TextEditingController();
  bool _senhaVisivel = false;
  bool _carregando = false;

  void _entrar() async {
    if (_credencial.text.isEmpty || _senha.text.isEmpty) return;
    setState(() => _carregando = true);
    await Future.delayed(const Duration(milliseconds: 800));
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const HomeScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 32),
              _buildLogo(),
              const SizedBox(height: 40),
              Text('Acesso CICC',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontWeight: FontWeight.w800,
                        color: AppColors.text,
                      )),
              const SizedBox(height: 4),
              Text('Identifique-se para acessar o painel',
                  style: TextStyle(color: Colors.grey[600], fontSize: 14)),
              const SizedBox(height: 32),
              TextFormField(
                controller: _credencial,
                decoration: const InputDecoration(
                  labelText: 'Credencial ou Matrícula',
                  hintText: 'Ex: TO-4921 ou email@to.gov.br',
                  prefixIcon: Icon(Icons.person_outline),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _senha,
                obscureText: !_senhaVisivel,
                decoration: InputDecoration(
                  labelText: 'Senha de Acesso',
                  hintText: '••••••••',
                  prefixIcon: const Icon(Icons.lock_outline),
                  suffixIcon: IconButton(
                    icon: Icon(_senhaVisivel
                        ? Icons.visibility_off_outlined
                        : Icons.visibility_outlined),
                    onPressed: () =>
                        setState(() => _senhaVisivel = !_senhaVisivel),
                  ),
                ),
              ),
              const SizedBox(height: 8),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(
                  onPressed: () {},
                  child: const Text('Esqueceu a senha?',
                      style: TextStyle(color: AppColors.river)),
                ),
              ),
              const SizedBox(height: 16),
              _carregando
                  ? const Center(
                      child: CircularProgressIndicator(color: AppColors.cerrado))
                  : ElevatedButton.icon(
                      onPressed: _entrar,
                      icon: const Icon(Icons.arrow_forward),
                      label: const Text('Autenticar Acesso'),
                    ),
              const SizedBox(height: 32),
              Center(
                child: TextButton(
                  onPressed: () {},
                  child: const Text(
                    'Solicitar Cadastro ao Naturatins →',
                    style: TextStyle(color: AppColors.river, fontSize: 13),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLogo() {
    return Row(
      children: [
        Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: AppColors.cerrado,
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Icon(Icons.eco, color: Colors.white, size: 24),
        ),
        const SizedBox(width: 12),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Canindé',
                style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w800,
                    color: AppColors.cerrado)),
            Text('SEMARH / TO',
                style: TextStyle(
                    fontSize: 10,
                    letterSpacing: 2,
                    color: Colors.grey[500],
                    fontWeight: FontWeight.w700)),
          ],
        ),
      ],
    );
  }
}
