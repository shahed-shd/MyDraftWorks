import 'package:bloc/bloc.dart';
import 'package:flutter_app_bloc/ui/main/dashboard/dashboard_state.dart';

import 'dashboard_event.dart';

class DashboardBloc extends Bloc<DashboardEvent, DashboardState>{
    @override
    DashboardState get initialState => InitialState();

    @override
    Stream<DashboardState> mapEventToState(DashboardEvent event) async* {
        if(event is ButtonOnePressed){
            yield ButtonPressedState('Button One');
        } else if(event is ButtonTwoPressed){
            yield ButtonPressedState('Button Two');
        }
    }
}
