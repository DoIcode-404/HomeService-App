import 'package:carousel_slider/carousel_slider.dart';
import 'package:client/modules/home/components/offers_card.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:flutter/material.dart';

class OfferList extends StatelessWidget {
  const OfferList({super.key});

  @override
  Widget build(BuildContext context) {
    return PrimaryContainer(
      height: 200,
      padding: EdgeInsets.only(top: 16, bottom: 16),
      child: CarouselSlider(
        options: CarouselOptions(
          height: 200,
          autoPlay: true,
          viewportFraction: 0.9,
          autoPlayAnimationDuration: const Duration(seconds: 2),
        ),
        items:
            [1, 2, 3, 4, 5].map((i) {
              return Builder(
                builder: (BuildContext context) {
                  return const OffersCard();
                },
              );
            }).toList(),
      ),
    );
  }
}
