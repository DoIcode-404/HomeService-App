import 'package:animations/animations.dart';
import 'package:client/data/constants/constants.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/components/rating_widget.dart';
import 'package:client/modules/categories/services_detail_view.dart';
import 'package:client/modules/widgets/animations/heart_animation.dart';

import 'package:flutter/material.dart';

class SubCategoryGridCard extends StatefulWidget {
  final ServicesModel service;

  const SubCategoryGridCard({super.key, required this.service});

  @override
  State<SubCategoryGridCard> createState() => _SubCategoryGridCardState();
}

class _SubCategoryGridCardState extends State<SubCategoryGridCard> {
  bool isFavorite = false;
  @override
  Widget build(BuildContext context) {
    bool isDarkMode(BuildContext context) =>
        Theme.of(context).brightness == Brightness.dark;

    return OpenContainer(
      transitionType: ContainerTransitionType.fadeThrough,
      openBuilder: (BuildContext _, VoidCallback openContainer) {
        return ServicesDetailView(services: widget.service);
      },
      middleColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,
      openColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,
      closedColor:
          isDarkMode(context) ? AppColors.kDarkSurfaceColor : AppColors.kWhite,
      closedShape: const RoundedRectangleBorder(),
      closedElevation: 0.0,
      closedBuilder: (BuildContext _, VoidCallback openContainer) {
        return GestureDetector(
          onTap: openContainer,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 147,
                height: 158,
                alignment: Alignment.topRight,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  image: DecorationImage(
                    image: AssetImage(widget.service.image),
                    fit: BoxFit.cover,
                  ),
                ),
                child: HeartAnimationWidget(
                  isAnimating: isFavorite,
                  duration: const Duration(milliseconds: 150),
                  child: IconButton(
                    onPressed: () {
                      setState(() {
                        isFavorite = !isFavorite;
                      });
                    },
                    icon: Icon(
                      isFavorite
                          ? Icons.favorite
                          : Icons.favorite_border_rounded,
                      color: isFavorite ? Colors.red : AppColors.kWhite,
                    ),
                  ),
                ),
              ),
              const Spacer(),
              Text(widget.service.name, style: AppTypography.kMedium14),
              SizedBox(height: 4),
              Text(
                'Starts From',
                style: AppTypography.kLight12.copyWith(
                  color: AppColors.kNeutral04.withOpacity(0.75),
                ),
              ),
              SizedBox(height: 5),
              Row(
                children: [
                  Container(
                    padding: EdgeInsets.symmetric(vertical: 4.5, horizontal: 8),
                    decoration: BoxDecoration(
                      color: AppColors.kLime,
                      borderRadius: BorderRadius.circular(5),
                    ),
                    child: Text(
                      '\$ ${widget.service.price}',
                      style: AppTypography.kMedium12,
                    ),
                  ),
                  const Spacer(),
                  SecondaryRatingWidget(service: widget.service),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
