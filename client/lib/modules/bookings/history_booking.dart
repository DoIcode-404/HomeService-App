import 'package:client/model/booking_model.dart';
import 'package:client/modules/bookings/components/history_booking_card.dart';
import 'package:flutter/material.dart';

class HistoryBookings extends StatelessWidget {
  const HistoryBookings({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      itemCount: historyBookings.length,
      padding: EdgeInsets.symmetric(horizontal: 20),
      separatorBuilder: (context, index) => SizedBox(height: 10),
      itemBuilder: (context, index) {
        return HistoryBookingCard(booking: historyBookings[index]);
      },
    );
  }
}
