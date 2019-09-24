import 'package:equatable/equatable.dart';

abstract class DashboardEvent extends Equatable {
    DashboardEvent([List props = const []]) : super(props);
}

class ButtonOnePressed extends DashboardEvent {

}

class ButtonTwoPressed extends DashboardEvent {

}
