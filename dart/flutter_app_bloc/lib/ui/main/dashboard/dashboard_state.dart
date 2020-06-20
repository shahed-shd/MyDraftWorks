import 'package:equatable/equatable.dart';

abstract class DashboardState extends Equatable {
    DashboardState([List props = const []]) : super(props);
}

class ButtonPressedState extends DashboardState{
    final String buttonName;

    ButtonPressedState(this.buttonName): super([buttonName]);
}


class InitialState extends DashboardState {

}

