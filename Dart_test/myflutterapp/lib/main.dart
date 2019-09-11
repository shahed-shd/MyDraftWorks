import 'package:flutter/material.dart';
import 'package:english_words/english_words.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        final word_pair = WordPair.random();
        return MaterialApp(
            title: 'Welcome to Flutter',
            home: Scaffold(
                appBar: AppBar(
                    title: Text('Welcome to Flutter'),
                ),
                body: Center(
                    // child: Text('Hello World'),
                    child: Text(word_pair.asPascalCase),
                ),
            ),
        );
    }
}