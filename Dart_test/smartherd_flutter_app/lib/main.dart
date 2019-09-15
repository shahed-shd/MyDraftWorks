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
        ),
    ));
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
                onTap: () => debugPrint("${listItems[index]} has been tapped"),
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
