import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Logic {
  Future<int> fetchQuantity() async {
    final response = await http
        .get(Uri.parse('http://10.0.2.2:5000/text'))
        .timeout(Duration(seconds: 5));
    String quantity = response.body;

    return int.parse(quantity);
  }
}

class SecondScreen extends StatefulWidget {
  @override
  _SecondScreenState createState() => _SecondScreenState();
}

class _SecondScreenState extends State<SecondScreen> {
  final double textSize = 22;
  final double videocardTextSize = 20;

  // final int itemCount = 50;

  String name = '';
  String price = '';
  List elems = [];

  Future fetchData(int index) async {
    final response = await http.get(Uri.parse('http://10.0.2.2:5000/text'));
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      print(data[index]['description']);
      // return [data[index]['description'], data[index]['price']];
      name = data[index]['description'];
      price = data[index]['price'];
    } else {
      print("Ошибка загрузки данных");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF1E1E2E),
    );
  }
}
