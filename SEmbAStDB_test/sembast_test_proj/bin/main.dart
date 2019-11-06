import 'package:sembast/sembast.dart';
import 'package:sembast/sembast_io.dart';

void main() async {
  print("Hello SEmbASt DB");

  // Opening a database
  String dbPath = 'sample.db';
  DatabaseFactory dbFactory = databaseFactoryIo;
  Database db = await dbFactory.openDatabase(dbPath);

  print(db.runtimeType);
}
