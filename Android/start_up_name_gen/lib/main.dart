// For basic flutter graphics
import 'package:flutter/material.dart';

// For dictionary of popular english words
import 'package:english_words/english_words.dart';

//
// **** A note on installing external packages **** //
// 
// The documentation on the package management system for Flutter
// suggests that it is quite primitive. To get an external package you must:
//
// 1) Find the source package name and version from https://pub.dartlang.org/flutter/
//
// 2) Edit pubspec.yaml in the root directory of your Flutter project:
//    
//  Example:
//
// dependencies:                      <- found in pubspec.yaml by default             
//   flutter:                         <- found in pubspec.yaml by default         
//     sdk: flutter                   <- found in pubspec.yaml by default          
//                                    <- found in pubspec.yaml by default
//   cupertino_icons: ^0.1.0          <- found in pubspec.yaml by default
//   english_words: ^3.1.0            <- THIS IS AN EXTERNAL PACKAGE (add this to the .yaml file)
//                                       its format is: <package_name>: ^<version_number>
//                                       here I am using english_words version 3.1.0 as an example
//
// 3) Run: 
//      > flutter packages get
//    From CLI
//

// The => (Fat Arrow) notation is used to denote a one-line function
void main() => runApp(new MyApp()); 

//
// Nearly everything in Flutter is a widget, which is just another
// term for identifying a code entity. Widgets can be created using
// other widgets.
// 
// For example:
//
// new Scaffold(                                  <- Scaffold is a widget
//   appBar: new AppBar(                          <- AppBar is a widget
//     title: new Text('Company Names'),          <- Text is a widget
// )
//
// The Scaffold widget is composed of an AppBar widget which is composed of a Text widget.
//

//
// This class is stateless - meaning it cannot change while
// the app is in use. 
//
// build determines how widgets are drawn to the screen
// final means this variable can be set only once - it
// should be used in stateless classes because they are
// not suppose to change after being initialized.
//
class MyApp extends StatelessWidget { 
  @override
  Widget build(BuildContext context) {          
    return new MaterialApp(
      title: 'Start-up Name Generator',
      theme: new ThemeData(
        primaryColor: Colors.lightGreenAccent,
      ),
      home: new RandomWords(),
    );
  }
}

//
// This class is stateful - meaning it CAN change while
// the app is in use. Think of RandomWords as a class that
// encompasses all random words in one big wrapper and RandomWordsState
// as the object that makes individual changes to each random word.
//
class RandomWords extends StatefulWidget { 
  @override
  createState() => new RandomWordsState();        // stateful widgets must create a state class
}

//
// State class for RandomWords - returns list of pascal-cased, random word pair
//
class RandomWordsState extends State<RandomWords> {
  final _names = <WordPair>[];              // _ is how to make a variable private in Dart
  final _biggerFont = const TextStyle(fontSize: 18.0);
  final _saved = new Set<WordPair>();

  Widget _buildCompanyNames() {
    return new ListView.builder(
      padding: const EdgeInsets.all(16.0),

      //
      // On even rows display the word pair
      // On odd rows, display a divider
      //
      // Looks like this:
      //
      // DustPlate
      // ----------
      // CoolDude
      // ----------
      // ...
      //
      itemBuilder: (context, wordCount) {
        if (wordCount.isOdd)
          return new Divider();

        final index = wordCount ~/ 2;                     // ~/ is integer divide
        if (index >= _names.length) {                     // Use lazy evaluation to add 10 more names                                                        // once the previous max has been generated
          _names.addAll(generateWordPairs().take(10));
        }
        return _buildRow(_names[index]);
      }
    );
  }

  Widget _buildRow(WordPair pair) {
    final alreadySaved = _saved.contains(pair);
    return new ListTile(
      title: new Text(
        pair.asPascalCase,
        style: _biggerFont,
      ),
      trailing: new Icon(
        alreadySaved ? Icons.favorite : Icons.favorite_border,
        color: alreadySaved ? Colors.red : null,
      ),
      onTap: () {
        setState(() {
          if (alreadySaved) {
            _saved.remove(pair);
          } else {
            _saved.add(pair);
          }
        });
      },
    );
  }

  void _pushSaved(){
    Navigator.of(context).push(
      new MaterialPageRoute(
      builder: (context) {
        final tiles = _saved.map(
          (pair) {
            return new ListTile(
              title: new Text(
                pair.asPascalCase,
                style: _biggerFont,
              ),
            );
          },
        );
        final divided = ListTile
          .divideTiles(
            context: context,
            tiles: tiles,
          )
          .toList();

        return new Scaffold(
          appBar: new AppBar(
            title: new Text('Saved Names'),
          ),
          body: new ListView(children: divided),
        );
      },
    ),
    );
  }

  @override
  Widget build(BuildContext context) {         
    return new Scaffold (
      appBar: new AppBar(
        title: new Text('Name Generator'),
        actions: <Widget>[
          new IconButton(icon: new Icon(Icons.list), onPressed: _pushSaved),
        ],
      ),
      body: _buildCompanyNames(),
    );
  }
}

