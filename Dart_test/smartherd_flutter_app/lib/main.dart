import 'package:flutter/material.dart';
import 'app_screens/home.dart';


void main() {
    runApp(
        MaterialApp(
            debugShowCheckedModeBanner: false,
            title: 'Simple Interest Calculator APP',
            home: SIForm(),
            theme: ThemeData(
                brightness: Brightness.dark,
                primaryColor: Colors.indigo,
                accentColor: Colors.indigo,
            ),
        )
    );
}


class SIForm extends StatefulWidget {

    @override
    State<StatefulWidget> createState() {
        return _SIFormState();
    }
}


class _SIFormState extends State<SIForm> {
    static var _currencies = ['BDT', 'Rupees', 'Dollars', 'Pounds'];
    final _minimumPadding = 5.0;

    var _currentItemSelected = '';

    TextEditingController principalController = TextEditingController();
    TextEditingController roiController = TextEditingController();
    TextEditingController termController = TextEditingController();

    var displayResult = '';

    @override
    void initState() {
        super.initState();
        _currentItemSelected = _currencies.first;
    }

    @override
    Widget build(BuildContext context) {
        TextStyle textStyle = Theme.of(context).textTheme.title;

        return Scaffold(
//            resizeToAvoidBottomPadding: false,
            appBar: AppBar(
                title: Text('Simple Interest Calculator'),
            ),
            body: Container(
//                margin: EdgeInsets.all(_minimumPadding * 2),
                child: ListView(
                    children: <Widget>[
                        getImageAsset(),

                        Padding(
                            padding: EdgeInsets.only(top: _minimumPadding, bottom: _minimumPadding),
                            child: TextField(
                                keyboardType: TextInputType.number,
                                style: textStyle,
                                controller: principalController,
                                decoration: InputDecoration(
                                    labelText: 'Principal',
                                    hintText: 'Enter Principal e.g. 12000',
                                    labelStyle: textStyle,
                                    border: OutlineInputBorder(
                                        borderRadius: BorderRadius.circular(5.0),
                                    ),
                                ),
                            ),
                        ),

                        Padding(
                            padding: EdgeInsets.only(top: _minimumPadding, bottom: _minimumPadding),
                            child: TextField(
                                keyboardType: TextInputType.number,
                                style: textStyle,
                                controller: roiController,
                                decoration: InputDecoration(
                                    labelText: 'Rate of Interest',
                                    hintText: 'In percent',
                                    labelStyle: textStyle,
                                    border: OutlineInputBorder(
                                        borderRadius: BorderRadius.circular(5.0),
                                    ),
                                ),
                            ),
                        ),

                        Padding(
                            padding: EdgeInsets.only(top: _minimumPadding, bottom: _minimumPadding),
                            child: Row(
                                children: <Widget>[
                                    Expanded(
                                        child: TextField(
                                            keyboardType: TextInputType.number,
                                            style: textStyle,
                                            controller: termController,
                                            decoration: InputDecoration(
                                                labelText: 'Term',
                                                hintText: 'Time in years',
                                                labelStyle: textStyle,
                                                border: OutlineInputBorder(
                                                    borderRadius: BorderRadius.circular(5.0),
                                                ),
                                            ),
                                        ),
                                    ),

                                    Container(width: _minimumPadding * 5),

                                    Expanded(
                                        child: DropdownButton<String>(
                                            items: _currencies.map((String value) {
                                                return DropdownMenuItem(
                                                    value: value,
                                                    child: Text(value),
                                                );
                                            }).toList(),

                                            value: _currentItemSelected,

                                            onChanged: (String newValueSelected) {
                                                _onDropDownItemSelected(newValueSelected);
                                            },
                                        ),
                                    ),
                                ],
                            ),
                        ),

                        Padding(
                            padding: EdgeInsets.only(top: _minimumPadding, bottom: _minimumPadding),
                            child: Row(
                                children: <Widget>[
                                    Expanded(
                                        child: RaisedButton(
                                            color: Theme.of(context).accentColor,
                                            textColor: Theme.of(context).primaryColorDark,
                                            child: Text('Calculate', textScaleFactor: 1.5),
                                            onPressed: () {
                                                setState(() {
                                                    this.displayResult = _calculateTotalReturn();
                                                });
                                            },
                                        ),
                                    ),

                                    Expanded(
                                        child: RaisedButton(
                                            color: Theme.of(context).primaryColorDark,
                                            textColor: Theme.of(context).primaryColorLight,
                                            child: Text('Reset', textScaleFactor: 1.5),
                                            onPressed: () {
                                                setState(() {
                                                    _reset();
                                                });
                                            },
                                        ),
                                    )
                                ],
                            ),
                        ),

                        Padding(
                            padding: EdgeInsets.only(top: _minimumPadding, bottom: _minimumPadding),
                            child: Text(this.displayResult),
                        )

                    ],
                ),
            ),
        );
    }

    Widget getImageAsset() {
        AssetImage assetImage = AssetImage('images/money.png');
        Image image = Image(image: assetImage, width: 125.0, height: 125);
        return Container(child: image, margin: EdgeInsets.all(_minimumPadding * 10));
    }

    void _onDropDownItemSelected(String newValueSelected) {
        setState(() {
            this._currentItemSelected = newValueSelected;
        });
    }

    String _calculateTotalReturn() {
        double principal = double.parse(principalController.text);
        double roi = double.parse(roiController.text);
        double term = double.parse(termController.text);

        double totalAmountPayble = principal + (principal * roi * term) / 100;

        String result = 'After $term years, your investment will be worth $totalAmountPayble';
        return result;
    }

    void _reset() {
        principalController.text = '';
        roiController.text = '';
        termController.text = '';
        displayResult = '';
        _currentItemSelected = _currencies.first;
    }
}


//void main() {
//    runApp(MaterialApp(
//        title: "Exploring UI Widgets",
//        home: Scaffold(
//            appBar: AppBar(
//                title: Text("Basic List View"),
//            ),
//            body: getListView(),
//            floatingActionButton: FloatingActionButton(
//                onPressed: () => debugPrint("FAB pressed"),
//                child: Icon(Icons.add),
//                tooltip: 'Add One More Item',
//            ),
//        ),
//    ));
//}
//
//
//void showTheSnackBar(BuildContext context, String item) {
//    var snackBar = SnackBar(
//        content: Text("You just tapped $item"),
//        action: SnackBarAction(
//            label: "UNDO",
//            onPressed: () {
//                debugPrint("Performing dummy UNDO operation");
//            },
//        ),
//    );
//
//    Scaffold.of(context).showSnackBar(snackBar);
//}
//
//
//List<String> getListElements() {
//    var items = List<String>.generate(1000, (counter) => "Item $counter");
//    return items;
//}
//
//
//Widget getListView() {
//    var listItems = getListElements();
//
//    var listView = ListView.builder(
//        itemBuilder: (context, index) {
////            debugPrint("itemBuilder called with index: $index");
//            return ListTile(
//                leading: Icon(Icons.arrow_right),
//                title: Text(listItems[index]),
//                onTap: () {
//                    debugPrint("${listItems[index]} has been tapped");
//                    showTheSnackBar(context, 'You just tapped ${listItems[index]}');
//                },
//            );
//        },
//    );
//
//    return listView;
//}


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
