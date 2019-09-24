import 'package:flutter/material.dart';
import 'package:flutter_app_bloc/ui/main/dashboard/dashboard_bloc.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'dashboard_event.dart';
import 'dashboard_state.dart';


class DashboardPage extends /*StatefulWidget*/ StatelessWidget {
//  @override
//  State<StatefulWidget> createState() {
//    return _DashboardPageState();
//  }
//}
//
//class _DashboardPageState extends State<DashboardPage> {

    @override
    Widget build(BuildContext context) {
        DashboardBloc _dashboardBloc = DashboardBloc();
        print("Dashboard page rebuild");

        return Scaffold(
            body: Center(
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                        BlocBuilder(
                            bloc: _dashboardBloc,
                            builder: (context, state) {
                                String str = "Undefined";

                                if (state is InitialState) {
                                  str = 'No button pressed';
                                } else if (state is ButtonPressedState) {
                                  str = '${state.buttonName} was pressed';
                                }
                                print("Text rebuild with state: $state");

                                return Text("$str");
                            },
                        ),

                        RaisedButton(
                            child: Text("Button One"),
                            onPressed: () {
                                print("onPressed called for Button One");
                                _dashboardBloc.dispatch(ButtonOnePressed());
//                                setState(() {
//                                    str = "Button one pressed";
//                                });
                            },
                        ),

                        RaisedButton(
                            child: Text("Button Two"),
                            onPressed: () {
                                print("onPressed called for Button Two");
                                _dashboardBloc.dispatch(ButtonTwoPressed());
//                                setState(() {
//                                    str = "Button two pressed";
//                                });
                            },
                        )
                    ],
                ),
            ),
        );
    }
}
