import 'package:sqflite/sqflite.dart';
import 'dart:async';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:smartherd_flutter_app/models/note.dart';


class DatabaseHelper {
    static DatabaseHelper _databaseHelper;      // Singleton DatabaseHelper
    static Database _database;                  // Singleton Database

    String noteTable = 'note_table';
    String colId = 'id';
    String colTitle = 'title';
    String colDescription = 'description';
    String colPriority = 'priority';
    String colDate = 'date';

    DatabaseHelper._createInstance();           // Named constructor to create instance of DatabaseHelper

    factory DatabaseHelper() {
        if(_databaseHelper == null) {
            _databaseHelper = DatabaseHelper._createInstance();
        }
        return _databaseHelper;
    }

    void _createDb(Database db, int newVersion) async {
        String sql = '''
        CREATE TABLE $noteTable (
            $colId INTEGER PRIMARY KEY AUTOINCREMENT,
            $colTitle TEXT,
            $colDescription TEXT,
            $colPriority INTEGER,
            $colDate TEXT
        )
        ''';

        await db.execute(sql);
    }

    Future<Database> initializeDatabase() async {
        // Get the directory path for both Android and iOS to store database.
        Directory directory = await getApplicationDocumentsDirectory();
        String path = directory.path + 'notes.db';

        // Open/crate the database at a given path.
        var notesDatabase = await openDatabase(path, version: 1, onCreate: _createDb);
        return notesDatabase;
    }

    Future<Database> get database async {
        if(_database == null) {
            _database = await initializeDatabase();
        }
        return _database;
    }

    // Fetch Operations: Get all Note objects from database.
    Future<List<Map<String, dynamic>>> getNoteMapList() async {
        Database db = await this.database;
        
//        var result = await db.rawQuery('SELECT * FROM $noteTable ORDER BY $colPriority ASC');
        var result = await db.query(noteTable, orderBy: '$colPriority ASC');
        return result;
    }

    // Insert Operations: Insert a Note object to database.
    Future<int> insertNote(Note note) async {
        Database db = await this.database;
        var result = await db.insert(noteTable, note.toMap());
        return result;
    }

    // Update Operations: Update a Note object and save it to database.
    Future<int> updateNote(Note note) async {
        Database db = await this.database;
        var result = await db.update(noteTable, note.toMap(), where: '$colId = ?', whereArgs: [note.id]);
        return result;
    }

    // Delete Operations: Delete a Note object from database.
    Future<int> deleteNote(int noteId) async {
        Database db = await this.database;
        var result = await db.rawDelete('DELETE FROM $noteTable WHERE $colId = $noteId');
        return result;
    }

    // Get number of Note objects ini database.
    Future<int> getCount() async {
        Database db = await this.database;
        List<Map<String, dynamic>> x = await db.rawQuery('SELECT COUNT(*) FROM $noteTable');
        int result = Sqflite.firstIntValue(x);
        return result;
    }

}
