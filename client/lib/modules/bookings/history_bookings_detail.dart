import 'package:client/data/constants/constants.dart';
import 'package:client/model/address_model.dart';
import 'package:client/model/booking_model.dart';
import 'package:client/modules/address/components/address_card.dart';
import 'package:client/modules/bookings/components/custom_expanded_tile.dart';
import 'package:client/modules/bookings/components/service_provider_card.dart';
import 'package:client/modules/categories/components/date_card.dart';
import 'package:client/modules/checkout/components/checkout_service_card.dart';
import 'package:client/modules/checkout/components/phone_number_card.dart';
import 'package:client/modules/checkout/components/promo_card.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class HistoryBookingsDetail extends StatelessWidget {
  final BookingModel bookings;
  const HistoryBookingsDetail({super.key, required this.bookings});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            SizedBox(height: 20),
            PrimaryContainer(
              child: Row(
                children: [
                  CustomHeaderText(text: 'Reference Code:', fontSize: 18),
                  SizedBox(width: 5),
                  Text(
                    bookings.referenceCode,
                    style: AppTypography.kBold16.copyWith(
                      color: const Color(0xFFFC944D),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
            const CheckoutServiceCard(),
            SizedBox(height: 16),
            const ServiceProviderCard(),
            SizedBox(height: 16),
            CustomExpandedTile(
              title: 'Address',
              children: [AddressCard(address: dummyAddresses[0])],
            ),
            SizedBox(height: 16),
            CustomExpandedTile(
              title: 'Date and Time',
              children: [
                DateCard(
                  onTap: null,
                  icon: AppAssets.kDate,
                  color: null,
                  title: 'Date',
                  subtitle: 'November 7, 2021',
                ),
                SizedBox(height: 10),
                DateCard(
                  onTap: null,
                  icon: AppAssets.kTime,
                  color: null,
                  title: 'Time',
                  subtitle: '12:00-01:00PM',
                ),
              ],
            ),
            SizedBox(height: 16),
            const CustomExpandedTile(
              title: 'Phone number',
              children: [PhoneNumberCard()],
            ),
            SizedBox(height: 16),
            const CustomExpandedTile(
              title: 'Promo Code',
              children: [PromoCard(isSelected: true)],
            ),
          ],
        ),
      ),
    );
  }
}
