import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import 'dart:convert';

class Logic {
  Future<Map<String, int>> fetchQuantity() async {
    final response = await http
        .get(Uri.parse('http://10.0.2.2:5000/checkVideocardsQuantity'));
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      // print(int);
      return {
        'cnt': data['qty']
      };
    } else {
      return 0;
    }
  }

  Future<Map<String, String?>> fetchData(int index) async {
    final response = await http
        .get(Uri.parse('http://10.0.2.2:5000/getVideoCard/$index'))
        .timeout(Duration(seconds: 5));
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return {
        'name': data['ProductName'] ?? '',
        'price': data['Price'] ?? ''
      };
    } else {
      return {
        'name': 'No data',
        'price': 'No data'
      };
    }
  }
}

// Первый экран, создание StatefulWidget
class CardsList extends StatefulWidget {
  @override
  // Прописываем обновление состояния
  _CardsListState createState() => _CardsListState();
}

// Как раз дефолтное состояние экрана
class _CardsListState extends State<CardsList> {
  final double textSize = 22;
  final double videocardTextSize = 20;

  // final int itemCount = 50;

  String name = '';
  String price = '';
  List elems = [];

  // Генерируем ключ сессии
  String uniqueId = Uuid().v4();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF1E1E2E),
      body: Center(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: 350),
          child: FutureBuilder(
            future: Logic().fetchQuantity(),
            builder: (context, snapshot) {
              return
                ListView.builder(
                  // shrinkWrap: true,
                  itemCount: snapshot.data,
                  itemBuilder: (context, index) {
                    return FutureBuilder(
                      future: Logic().fetchData(index),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState ==
                            ConnectionState.waiting) {
                          return SizedBox(
                            width: 50,
                            height: 50,
                            child: Center(
                                child: CircularProgressIndicator()),
                          );
                        } else if (snapshot.hasError) {
                          // Если произошла ошибка, показываем сообщение об ошибке
                          return Center(
                              child: Text('Ошибка: ${snapshot.error}'));
                        } else if (snapshot.hasData) {
                          return Padding(
                            padding: EdgeInsets.only(
                                top: 18, left: 10, right: 10),
                            child: Container(
                              width: 100,
                              height: 350,
                              padding: EdgeInsets.all(15.0),
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(10),
                                color: Color(0xFF3A3A4D),
                              ),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment
                                    .spaceBetween,
                                children: [
                                  SizedBox(
                                    child: Image.network(
                                      "http://10.0.2.2:5000/assets/$index",
                                      loadingBuilder: (context, child, loadingProgress) {
                                        if (loadingProgress == null) {
                                          return child;
                                        } else {
                                          return Center(child: CircularProgressIndicator());
                                        }
                                      },
                                      errorBuilder: (context, error, stackTrace) {
                                        return Container(
                                          color: Colors.grey[800],
                                          child: Center(
                                            child: Text(
                                              'Изображение недоступно',
                                              style: TextStyle(color: Colors.white, fontSize: 16),
                                              textAlign: TextAlign.center,
                                            )
                                          )
                                        );
                                      },
                                    ),
                                  ),
                                  Text(
                                    name,
                                    style: TextStyle(
                                        fontSize: videocardTextSize),
                                  ),
                                  Text(
                                    price,
                                    style: TextStyle(fontSize: textSize),
                                    textAlign: TextAlign.left,
                                  ),
                                ],
                              ),
                            ),
                          );
                        } else {
                          return SizedBox(
                            width: 50,
                            height: 50,
                            child: Center(
                              child: CircularProgressIndicator()
                            ),
                          );
                        }
                      },
                    );
                  },
                )
              ;
            }
          )
        ),
      ),
    );
  }
}
