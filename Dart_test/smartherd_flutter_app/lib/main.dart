import 'package:flutter/material.dart';
import 'app_screens/first_screen.dart';


void main() => runApp(MyFlutterApp());


class MyFlutterApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
      return MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'Smartherd Flutter App',
          home: Scaffold(
              appBar: AppBar(title: Text('My First App Screen'),),
              body: FirstScreen(),
          ),
      );
  }
}