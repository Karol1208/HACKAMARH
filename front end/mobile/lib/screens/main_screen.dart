import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'home_screen.dart';
import 'viveiro_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _tab = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _tab,
        children: const [HomeScreen(), ViveiroScreen()],
      ),
      bottomNavigationBar: _buildNav(),
    );
  }

  Widget _buildNav() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Colors.grey.shade100)),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 16, offset: const Offset(0, -4)),
        ],
      ),
      child: SafeArea(
        top: false,
        child: SizedBox(
          height: 58,
          child: Row(
            children: [
              _navItem(Icons.home_outlined, 0),
              _navItem(Icons.eco_outlined, 1),
              _navItem(Icons.person_outline, -1, onTap: () {
                Navigator.pushNamedAndRemoveUntil(context, '/', (r) => false);
              }),
            ],
          ),
        ),
      ),
    );
  }

  Widget _navItem(IconData icon, int index, {VoidCallback? onTap}) {
    final active = _tab == index;
    return Expanded(
      child: GestureDetector(
        onTap: onTap ?? () => setState(() => _tab = index),
        behavior: HitTestBehavior.opaque,
        child: Container(
          decoration: BoxDecoration(
            border: Border(
              top: BorderSide(
                color: active ? AppColors.cerrado : Colors.transparent,
                width: 2.5,
              ),
            ),
          ),
          child: Center(
            child: Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Icon(icon,
                  color: active ? AppColors.cerrado : Colors.grey.shade400, size: 24),
            ),
          ),
        ),
      ),
    );
  }
}
