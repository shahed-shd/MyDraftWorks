import 'package:flutter/material.dart';
import 'app_screens/home.dart';

void main() {
    runApp(MaterialApp(
        title: "Exploring UI Widgets",
        home: Scaffold(
            appBar: AppBar(
                title: Text("Basic List View"),
            ),
            body: getListView(),
            floatingActionButton: FloatingActionButton(
                onPressed: () => debugPrint("FAB pressed"),
                child: Icon(Icons.add),
                tooltip: 'Add One More Item',
            ),
        ),
    ));
}


void showTheSnackBar(BuildContext context, String item) {
    var snackBar = SnackBar(
        content: Text("You just tapped $item"),
        action: SnackBarAction(
            label: "UNDO",
            onPressed: () {
                debugPrint("Performing dummy UNDO operation");
            },
        ),
    );

    Scaffold.of(context).showSnackBar(snackBar);
}


List<String> getListElements() {
    var items = List<String>.generate(1000, (counter) => "Item $counter");
    return items;
}


Widget getListView() {
    var listItems = getListElements();

    var listView = ListView.builder(
        itemBuilder: (context, index) {
//            debugPrint("itemBuilder called with index: $index");
            return ListTile(
                leading: Icon(Icons.arrow_right),
                title: Text(listItems[index]),
                onTap: () {
                    debugPrint("${listItems[index]} has been tapped");
                    showTheSnackBar(context, 'You just tapped ${listItems[index]}');
                },
            );
        },
    );

    return listView;
}


//Widget getListView() {
//    var listView = ListView(
//        children: <Widget>[
//            ListTile(
//                leading: Icon(Icons.landscape),
//                title: Text("Landscape"),
//                subtitle: Text("Beautiful View !"),
//                trailing: Icon(Icons.wb_sunny),
//                onTap: () {
//                    debugPrint("Landscape tapped");
//                },
//                onLongPress: () {
//                    debugPrint("Landscape long pressed");
//                },
//            ),
//
//            ListTile(
//                leading: Icon(Icons.laptop_chromebook),
//                title: Text("Windows"),
//            ),
//
//            ListTile(
//                leading: Icon(Icons.phone),
//                title: Text("Phone"),
//            ),
//
//            Text("Yet another element in List"),
//
//            Container(color: Colors.red, height: 50.0,),
//        ],
//    );
//
//    return listView;
//}
