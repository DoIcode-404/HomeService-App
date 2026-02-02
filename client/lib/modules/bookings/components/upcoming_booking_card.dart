import 'package:client/data/constants/constants.dart';
import 'package:client/model/booking_model.dart';
import 'package:client/modules/bookings/components/booking_service_card.dart';
import 'package:client/modules/bookings/components/status_card.dart';
import 'package:client/modules/widgets/animations/button_animation.dart';
import 'package:client/modules/widgets/animations/fade_animations.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:flutter/material.dart';

import 'package:flutter_svg/flutter_svg.dart';
import 'package:intl/intl.dart';

class UpComingBookingCard extends StatelessWidget {
  final BookingModel bookings;
  const UpComingBookingCard({super.key, required this.bookings});

  @override
  Widget build(BuildContext context) {
    String formattedFromDate = DateFormat('h:mm').format(bookings.fromDate);
    String formattedToDate = DateFormat(
      'h:mm a, dd MMM',
    ).format(bookings.toDate);
    return FadeInAnimation(
      curve: Curves.easeIn,
      duration: const Duration(milliseconds: 500),
      child: PrimaryContainer(
        child: Column(
          children: [
            BookingServiceCard(booking: bookings),
            Divider(height: 25),
            Row(
              children: [
                Text('Status', style: AppTypography.kLight14),
                const Spacer(),
                BookingStatusCard(status: bookings.status),
              ],
            ),
            SizedBox(height: 10),
            Row(
              children: [
                Container(
                  height: 45,
                  width: 45,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: AppColors.kInput),
                  ),
                  child: SvgPicture.asset(
                    AppAssets.kDate,
                    colorFilter: const ColorFilter.mode(
                      AppColors.kGrey,
                      BlendMode.srcIn,
                    ),
                  ),
                ),
                SizedBox(width: 10),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$formattedFromDate-$formattedToDate',
                      style: AppTypography.kMedium14,
                    ),
                    Text(
                      'Schedule',
                      style: AppTypography.kLight12.copyWith(
                        color: AppColors.kNeutral04,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            SizedBox(height: 10),
            Row(
              children: [
                Container(
                  height: 45,
                  width: 45,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: AppColors.kInput),
                  ),
                  child: Image.asset(bookings.serviceProvider.profilePic),
                ),
                SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        bookings.serviceProvider.name,
                        style: AppTypography.kMedium14,
                      ),
                      Text(
                        'Service provider',
                        style: AppTypography.kLight12.copyWith(
                          color: AppColors.kNeutral04,
                        ),
                      ),
                    ],
                  ),
                ),
                ButtonAnimation(
                  child: Container(
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.kPrimary,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Row(
                      children: [
                        SvgPicture.asset(AppAssets.kCall),
                        SizedBox(width: 5),
                        Text(
                          'Call',
                          style: AppTypography.kMedium15.copyWith(
                            color: AppColors.kWhite,
                          ),
                        ),
                      ],
                    ),
                  ),
                  onTap: () {},
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
