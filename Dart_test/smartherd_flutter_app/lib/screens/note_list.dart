import 'package:flutter/material.dart';
import 'package:smartherd_flutter_app/screens/note_details.dart';


class NoteList extends StatefulWidget {

    @override
    State<StatefulWidget> createState() {
        return NoteListState();
    }
}


class NoteListState extends State<NoteList> {

    var count = 0;

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text("Notes"),
            ),

            body: getNoteListView(),

            floatingActionButton: FloatingActionButton(
                onPressed: () {
                    debugPrint('FAB pressed');
                    navigateToDetail('Add Note');
                },

                tooltip: 'Add Note',

                child: Icon(Icons.add),
            ),
        );
    }

    ListView getNoteListView() {
        TextStyle textStyle = Theme.of(context).textTheme.subhead;

        return ListView.builder(
            itemCount: count,
            itemBuilder: (BuildContext context, int position) {
                return Card(
                    color: Colors.white,
                    elevation: 2.0,
                    child: ListTile(
                        leading: CircleAvatar(
                            backgroundColor: Colors.yellow,
                            child: Icon(Icons.keyboard_arrow_right),
                        ),

                        title: Text('Dummy Title', style: textStyle),

                        subtitle: Text('Dummy Date'),

                        trailing: Icon(Icons.delete, color: Colors.grey),

                        onTap: () {
                            debugPrint("ListTile tapped");
                            navigateToDetail('Edit Note');
                        },
                    ),
                );
            },
        );
    }

    void navigateToDetail(String title) {
        Navigator.push(context, MaterialPageRoute(builder: (context) {
            return NoteDetail(title);
        }));
    }
}