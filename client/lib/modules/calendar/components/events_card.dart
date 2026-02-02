import 'package:client/data/constants/constants.dart';
import 'package:client/model/events.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:intl/intl.dart';

class EventCard extends StatelessWidget {
  final Event event;
  const EventCard({required this.event, super.key});

  @override
  Widget build(BuildContext context) {
    final fromTimeFormatted = DateFormat('h:mm a').format(event.fromTime);
    final toTimeFormatted = DateFormat('h:mm a').format(event.toTime);

    return Row(
      children: [
        Container(
          height: 55,
          width: 5,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: event.category.color,
          ),
          child: SvgPicture.asset(event.category.image),
        ),
        SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(event.title, style: AppTypography.kMedium16),
            SizedBox(height: 5),
            Text(
              '$fromTimeFormatted - $toTimeFormatted',
              style: AppTypography.kLight14.copyWith(color: AppColors.kNeutral),
            ),
          ],
        ),
      ],
    );
  }
}
