import 'package:english_words/english_words.dart' as prefix0;
import 'package:flutter/material.dart';
import 'package:english_words/english_words.dart';


void main() => runApp(MyApp());


class RandomWordsState extends State<RandomWords> {
    final _suggestions = <WordPair>[];
    final _biggerFont = const TextStyle(fontSize: 18.0);

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Startup Name Generator'),
            ),
            body: _buildSuggestions(),
        )
        // final wordPair = WordPair.random();
        // return Text(wordPair.asPascalCase);
    }

    Widget _buildRow(WordPair pair) {
        return ListTile(
            title: Text(
                pair.asPascalCase,
                style: _biggerFont,
            ),
        );
    }

    Widget _buildSuggestions() {
        return ListView.builder(
            padding: const EdgeInsets.all(16.0),
            itemBuilder: (context, i) {
                if(i.isOdd) return Divider();

                final index = i ~/ 2;
                if(index >= _suggestions.length) {
                    _suggestions.addAll(generateWordPairs().take(10));
                }
                return _buildRow(_suggestions[index]);
            },
        );
    }
}


class RandomWords extends StatefulWidget {
    @override
    RandomWordsState createState() => RandomWordsState();
}


class MyApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        // final word_pair = WordPair.random();
        return MaterialApp(
            title: 'Startup Name Generator',
            home: RandomWords(),
            // title: 'Welcome to Flutter',
            // home: Scaffold(
            //     appBar: AppBar(
            //         title: Text('Welcome to Flutter'),
            //     ),
            //     body: Center(
            //         // child: Text('Hello World'),
            //         // child: Text(word_pair.asPascalCase),
            //         child: RandomWords(),
            //     ),
            // ),
        );
    }
}