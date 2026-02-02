import 'package:client/data/constants/constants.dart';
import 'package:client/model/booking_model.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/svg.dart';

class BookingServiceCard extends StatelessWidget {
  final BookingModel booking;
  const BookingServiceCard({super.key, required this.booking});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          height: 55,
          width: 55,
          padding: EdgeInsets.all(17),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: booking.service.category.color,
          ),
          child: SvgPicture.asset(booking.service.category.image),
        ),
        SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(booking.service.name, style: AppTypography.kMedium16),
            SizedBox(height: 5),
            Text(
              'Reference Code: #${booking.referenceCode}',
              style: AppTypography.kLight14.copyWith(color: AppColors.kNeutral),
            ),
          ],
        ),
      ],
    );
  }
}
