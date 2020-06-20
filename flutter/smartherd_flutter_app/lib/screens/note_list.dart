import 'dart:async';
import 'package:flutter/material.dart';
import 'package:smartherd_flutter_app/screens/note_details.dart';
import 'package:smartherd_flutter_app/models/note.dart';
import 'package:smartherd_flutter_app/utils/database_helper.dart';
import 'package:sqflite/sqflite.dart';


class NoteList extends StatefulWidget {

    @override
    State<StatefulWidget> createState() {
        return NoteListState();
    }
}


class NoteListState extends State<NoteList> {

    DatabaseHelper databaseHelper = DatabaseHelper();
    List<Note> noteList;
    int count = 0;

    @override
    Widget build(BuildContext context) {
        if(noteList == null) {
            noteList = List<Note>();
            updateListView();
        }

        return Scaffold(
            appBar: AppBar(
                title: Text("Notes"),
            ),

            body: getNoteListView(),

            floatingActionButton: FloatingActionButton(
                onPressed: () {
                    debugPrint('FAB pressed');
                    navigateToDetail(Note('', '', 1), 'Add Note');
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
                Note currentNote = this.noteList[position];
                return Card(
                    color: Colors.white,
                    elevation: 2.0,
                    child: ListTile(
                        leading: CircleAvatar(
                            backgroundColor: getPriorityColor(currentNote.priority),
                            child: getPriorityIcon(currentNote.priority),
                        ),

                        title: Text(currentNote.title, style: textStyle),

                        subtitle: Text(currentNote.date),

                        trailing: GestureDetector(
                            child: Icon(Icons.delete, color: Colors.grey),
                            onTap: () {
                                _delete(context, currentNote);
                            },
                        ),

                        onTap: () {
                            debugPrint("ListTile tapped");
                            navigateToDetail(currentNote, 'Edit Note');
                        },
                    ),
                );
            },
        );
    }

    // Returns the priority color.
    Color getPriorityColor(int priority) {
        Color color;

        switch(priority) {
            case 1:
                color = Colors.yellow;
                break;
            case 2:
                color = Colors.red;
                break;
            default:
                color = Colors.yellow;
        }

        return color;
    }

    // Return the priority icon.
    Icon getPriorityIcon(int priority) {
        Icon icon;

        switch(priority) {
            case 1:
                icon = Icon(Icons.keyboard_arrow_right);
                break;
            case 2:
                icon = Icon(Icons.play_arrow);
                break;
            default:
                icon = Icon(Icons.keyboard_arrow_right);
        }

        return icon;
    }

    void _delete(BuildContext context, Note note) async {
        int result = await databaseHelper.deleteNote(note.id);
        if(result != 0) {
            _showSnackBar(context, 'Note Deleted Successfully');
            updateListView();
        }
    }

    void _showSnackBar(BuildContext context, String message) {
        final snackBar = SnackBar(content: Text(message));
        Scaffold.of(context).showSnackBar(snackBar);
    }

    void navigateToDetail(Note note, String title) async {
        bool result = await Navigator.push(context, MaterialPageRoute(builder: (context) {
            return NoteDetail(note, title);
        }));

        if(result == true) {
            updateListView();
        }
    }

    void updateListView() {
        final Future<Database> dbFuture = databaseHelper.initializeDatabase();
        dbFuture.then((database) {
            Future<List<Note>> noteListFuture = databaseHelper.getNoteList();
            noteListFuture.then((noteList) {
                setState(() {
                    this.noteList = noteList;
                    this.count = noteList.length;
                });
            });
        });
    }
}