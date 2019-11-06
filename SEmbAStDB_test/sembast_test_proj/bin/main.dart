import 'package:sembast/sembast.dart';
import 'package:sembast/sembast_io.dart';

void main() async {
  print("Hello SEmbASt DB");

  // Opening a database
  String dbPath = 'sample.db';
  DatabaseFactory dbFactory = databaseFactoryIo;
  Database db = await dbFactory.openDatabase(dbPath);

  // Reading and writing
  var store = StoreRef.main();
  await store.record('title').put(db, 'Simple application');
  await store.record('version').put(db, 10);
  await store.record('settings').put(db, {'offline': true});
  await store.record('version').delete(db);

  var intMapStore = intMapStoreFactory.store('animals');  // int map
  await db.transaction((txn) async {
    await intMapStore.add(txn, {'name': 'fish'});
    await intMapStore.add(txn, {'name': 'cat'});
  });

  var storeTyped = StoreRef<String, String>.main();   // strong mode to make database access less error prone
  await storeTyped.record('username').put(db, 'my_username');
  await storeTyped.record('url').put(db, 'my_url');

  var url = await storeTyped.record('url').get(db);
  var username = await storeTyped.record('username').get(db);
  print("$url, $username");

  await db.close();
}
