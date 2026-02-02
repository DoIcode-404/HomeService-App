import 'package:client/model/booking_model.dart';
import 'package:client/modules/bookings/components/upcoming_booking_card.dart';
import 'package:flutter/material.dart';

class UpComingBookings extends StatelessWidget {
  const UpComingBookings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      itemCount: upcomingBookings.length,
      padding: EdgeInsets.symmetric(horizontal: 20),
      separatorBuilder: (context, index) => SizedBox(height: 10),
      itemBuilder: (context, index) {
        return UpComingBookingCard(bookings: upcomingBookings[index]);
      },
    );
  }
}
