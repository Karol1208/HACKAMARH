import 'dart:convert';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

class ApiService {
  static final _base = kIsWeb ? 'http://localhost:8000' : 'http://10.0.2.2:8000';

  // --- RN01: Alerta Cidadão ---
  static Future<Map<String, dynamic>> enviarAlertaIncendio(XFile imagem) async {
    final uri = Uri.parse('$_base/alertas/incendio');
    final request = http.MultipartRequest('POST', uri);
    final bytes = await imagem.readAsBytes();
    request.files.add(
      http.MultipartFile.fromBytes('imagem', bytes, filename: imagem.name),
    );
    final streamed = await request.send().timeout(const Duration(seconds: 10));
    final body = await streamed.stream.bytesToString();
    return jsonDecode(body) as Map<String, dynamic>;
  }

  // --- RN04: Scanner de Restauração ---
  static Future<Map<String, dynamic>> analisarMuda(XFile imagem) async {
    final uri = Uri.parse('$_base/scanner/muda');
    final request = http.MultipartRequest('POST', uri);
    final bytes = await imagem.readAsBytes();
    request.files.add(
      http.MultipartFile.fromBytes('imagem', bytes, filename: imagem.name),
    );
    final streamed = await request.send().timeout(const Duration(seconds: 15));
    final body = await streamed.stream.bytesToString();
    return jsonDecode(body) as Map<String, dynamic>;
  }

  // --- Dashboard KPIs ---
  static Future<Map<String, dynamic>> kpis() async {
    final res = await http
        .get(Uri.parse('$_base/dashboard/kpis'))
        .timeout(const Duration(seconds: 5));
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}
