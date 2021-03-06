import 'dart:async';
import 'package:flutter/material.dart';
import 'package:smartherd_flutter_app/models/note.dart';
import 'package:smartherd_flutter_app/utils/database_helper.dart';
import 'package:intl/intl.dart';


class NoteDetail extends StatefulWidget {
    final String appBarTitle;
    final Note note;

    NoteDetail(Note this.note, this.appBarTitle);

    @override
    State<StatefulWidget> createState() {
        return NoteDetailState(this.note, this.appBarTitle);
    }
}


class NoteDetailState extends State<NoteDetail> {

    static var _priorities = ['Low', 'High'];

    var _formKey = GlobalKey<FormState>();
    DatabaseHelper helper = DatabaseHelper();

    String appBarTitle;
    Note note;

    TextEditingController titleController = TextEditingController();
    TextEditingController descriptionController = TextEditingController();

    NoteDetailState(this.note, this.appBarTitle);

    @override
    Widget build(BuildContext context) {
        TextStyle textStyle = Theme.of(context).textTheme.title;

        titleController.text = note.title;
        descriptionController.text = note.description;

        return WillPopScope(
            onWillPop: () {
                // Write some code to control things, when user press back button.
                moveToLastScreen();
            },

            child: Scaffold(
                appBar: AppBar(
                    leading: IconButton(
                        icon: Icon(Icons.arrow_back),
                        onPressed: () {
                            // Write some code to control things, when user press back button.
                            moveToLastScreen();
                        },
                    ),
                    title: Text(this.appBarTitle),
                ),
                body: Form(
                    key: _formKey,
                    child: Padding(
                        padding: EdgeInsets.only(top: 15.0, left: 10.0, right: 10.0),
                        child: ListView(
                            children: <Widget>[
                                ListTile(
                                    // First element.
                                    title: DropdownButton(
                                        items: _priorities.map((String dropdownStringItem) {
                                            return DropdownMenuItem<String>(
                                                value: dropdownStringItem,
                                                child: Text(dropdownStringItem),
                                            );
                                        }).toList(),

                                        style: textStyle,

                                        value: getPriorityAsString(note.priority),

                                        onChanged: (valueSelectedByUser) {
                                            setState(() {
                                                debugPrint('User selected $valueSelectedByUser');
                                                updatePriorityAsInt(valueSelectedByUser);
                                            });
                                        },
                                    ),
                                ),

                                // Second element.
                                Padding(
                                    padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
                                    child: TextFormField(
                                        controller: titleController,
                                        style: textStyle,
                                        onChanged: (value) {
                                            debugPrint('Something changed in Title Text Field');
                                            updateTitle();
                                        },
                                        validator: (String value) {
                                            if(value.isEmpty) {
                                                return 'Please, enter a title for the note';
                                            }
                                            return null;
                                        },
                                        decoration: InputDecoration(
                                            labelText: 'Title',
                                            labelStyle: textStyle,
                                            border: OutlineInputBorder(
                                                borderRadius: BorderRadius.circular(5.0),
                                            )
                                        ),
                                    ),
                                ),

                                // Third element.
                                Padding(
                                    padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
                                    child: TextFormField(
                                        controller: descriptionController,
                                        style: textStyle,
                                        onChanged: (value) {
                                            debugPrint('Something changed in Description Text Field');
                                            updateDescription();
                                        },
                                        decoration: InputDecoration(
                                            labelText: 'Description',
                                            labelStyle: textStyle,
                                            border: OutlineInputBorder(
                                                borderRadius: BorderRadius.circular(5.0),
                                            )
                                        ),
                                    ),
                                ),

                                // Fourth element.
                                Padding(
                                    padding: EdgeInsets.only(top: 15.0, bottom: 15.0),
                                    child: Row(
                                        children: <Widget>[
                                            Expanded(
                                                child: RaisedButton(
                                                    color: Theme.of(context).primaryColorDark,
                                                    textColor: Theme.of(context).primaryColorLight,
                                                    child: Text(
                                                        'Save',
                                                        textScaleFactor: 1.5,
                                                    ),
                                                    onPressed: () {

                                                        setState(() {
                                                            if(_formKey.currentState.validate()) {
                                                                debugPrint("Save button clicked");
                                                                _save();
                                                            }
                                                        });
                                                    },
                                                ),
                                            ),

                                            Container(width: 5.0,),

                                            Expanded(
                                                child: RaisedButton(
                                                    color: Theme.of(context).primaryColorDark,
                                                    textColor: Theme.of(context).primaryColorLight,
                                                    child: Text(
                                                        'Delete',
                                                        textScaleFactor: 1.5,
                                                    ),
                                                    onPressed: () {
                                                        setState(() {
                                                            debugPrint("Delete button clicked");
                                                            _delete();
                                                        });
                                                    },
                                                ),
                                            )
                                        ],
                                    ),
                                )
                            ],
                        ),
                    ),
                ),
            ),
        );
    }

    void moveToLastScreen() {
        Navigator.pop(context, true);
    }

    // Convert the String priority in the form of integer before saving it to Database.
    void updatePriorityAsInt(String value) {
        switch(value) {
            case 'Low':
                note.priority = 1;
                break;
            case 'High':
                note.priority = 2;
                break;
        }
    }

    // Convert int priority to String priority and display it to user in Dropdown.
    String getPriorityAsString(int value) {
        String priority;
        switch(value) {
            case 1:
                priority = _priorities[0];  // Low
                break;
            case 2:
                priority = _priorities[1];  // High
                break;
        }

        return priority;
    }

    // Update the title of Note object.
    void updateTitle() {
        note.title = titleController.text;
    }

    // Update the description of Note object.
    void updateDescription() {
        note.description = descriptionController.text;
    }

    // Save data to database.
    void _save() async {
        moveToLastScreen();

        note.date = DateFormat.yMMMd().format(DateTime.now());
        int result;

        if(note.id != null) {   // Case 1: Update operation.
            result = await helper.updateNote(note);
        } else {    // Case 2: Insert operation.
            result = await helper.insertNote(note);
        }

        if(result != 0) {   // Success.
            _showAlertDialogue('Status', 'Note Saved Successfully');
        } else {    // Failure
            _showAlertDialogue('Status', 'Problem Saving Note');
        }
    }

    void _delete() async {
        moveToLastScreen();

        // Case 1: If user is trying to delete the NEW NOTE i.e. he has come to the detail page by pressing the FAB of NoteList page.
        if(note.id == null) {
            _showAlertDialogue('Status', 'No Note was deleted');
            return;
        }

        // Case 2: User is trying to delete the old note that already has a valid ID.
        int result = await helper.deleteNote(note.id);
        if(result != 0) {
            _showAlertDialogue('Status', 'Note Deleted Successfully');
        } else {
            _showAlertDialogue('Status', 'Error Occured While Deleting Note');
        }
    }

    void _showAlertDialogue(String title, String message) {
        AlertDialog alertDialog = AlertDialog(
            title: Text(title),
            content: Text(message),
        );

        showDialog(
            context: context,
            builder: (_) => alertDialog,
        );
    }
}
