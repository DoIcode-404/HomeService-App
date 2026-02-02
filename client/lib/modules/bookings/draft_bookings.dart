import 'package:client/model/booking_model.dart';
import 'package:client/modules/bookings/components/draft_booking_card.dart';
import 'package:flutter/material.dart';

class DraftBookings extends StatelessWidget {
  const DraftBookings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      itemCount: draftsBookings.length,
      padding: EdgeInsets.symmetric(horizontal: 20),
      separatorBuilder: (context, index) => SizedBox(height: 10),
      itemBuilder: (context, index) {
        return DraftBookingCard(booking: draftsBookings[index]);
      },
    );
  }
}
