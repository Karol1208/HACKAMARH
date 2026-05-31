import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const _base = 'http://10.0.2.2:8000'; // emulador Android → localhost
  // Em device físico: trocar pelo IP da máquina, ex: http://192.168.1.x:8000

  // --- RN01: Alerta Cidadão ---
  static Future<Map<String, dynamic>> enviarAlertaIncendio(File imagem) async {
    final uri = Uri.parse('$_base/alertas/incendio');
    final request = http.MultipartRequest('POST', uri);
    request.files.add(await http.MultipartFile.fromPath('imagem', imagem.path));
    final streamed = await request.send().timeout(const Duration(seconds: 10));
    final body = await streamed.stream.bytesToString();
    return jsonDecode(body) as Map<String, dynamic>;
  }

  // --- RN04: Scanner de Restauração ---
  static Future<Map<String, dynamic>> analisarMuda(File imagem) async {
    final uri = Uri.parse('$_base/scanner/muda');
    final request = http.MultipartRequest('POST', uri);
    request.files.add(await http.MultipartFile.fromPath('imagem', imagem.path));
    final streamed = await request.send().timeout(const Duration(seconds: 15));
    final body = await streamed.stream.bytesToString();
    return jsonDecode(body) as Map<String, dynamic>;
  }

  // --- Dashboard KPIs ---
  static Future<Map<String, dynamic>> kpis() async {
    final res = await http.get(Uri.parse('$_base/dashboard/kpis'))
        .timeout(const Duration(seconds: 5));
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}
