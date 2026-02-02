import 'package:client/data/constants/constants.dart';
import 'package:client/model/category_model.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/all_categories_view.dart';
import 'package:client/modules/categories/components/category_card.dart';
import 'package:client/modules/home/components/home_appbar.dart';
import 'package:client/modules/home/components/home_services_card.dart';
import 'package:client/modules/home/components/offers_list.dart';
import 'package:client/modules/home/components/search_field.dart';
import 'package:client/modules/home/components/show_case_widget.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:showcaseview/showcaseview.dart';

class HomeView extends StatefulWidget {
  final GlobalKey<ScaffoldState> drawerKey;
  const HomeView({super.key, required this.drawerKey});

  @override
  State<HomeView> createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  final GlobalKey _one = GlobalKey();
  final GlobalKey _two = GlobalKey();
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    ambiguate(WidgetsBinding.instance)?.addPostFrameCallback(
      (_) => ShowCaseWidget.of(context).startShowCase([_one, _two]),
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: HomeAppBar(
        showCaseKey: _one,
        onLeadingPressed: () {
          widget.drawerKey.currentState?.openDrawer();
        },
        onShowCaseNextTap: () {
          ShowCaseWidget.of(context).next();
        },
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            SizedBox(height: 20),
            PrimaryContainer(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Hello Shameel 👋',
                    style: AppTypography.kMedium14.copyWith(
                      color: AppColors.kGrey,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'What you are looking for today',
                    style: AppTypography.kBold32,
                  ),
                  SizedBox(height: 14),
                  SearchField(
                    controller: _searchController,
                    onSearchPress: () {},
                  ),
                ],
              ),
            ),
            SizedBox(height: 16),
            const OfferList(),
            SizedBox(height: 16),
            Showcase.withWidget(
              key: _two,
              overlayOpacity: 0,
              height: 100,
              width: 300,
              disposeOnTap: false,
              container: CustomShowCaseWidget(
                buttonText: 'Got it',
                title: 'Choose your Categories',
                description:
                    'Lorem Ipsum is simply dummy text of the\nprinting and typesetting industry. ',
                onNextTap: () {
                  ShowCaseWidget.of(context).dismiss();
                },
                widgetNumber: '2',
              ),
              child: PrimaryContainer(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: List.generate(4, (index) {
                    if (index == 3) {
                      return CategorySeeAllButton(
                        onTap: () {
                          Get.to(() => const AllCategories());
                        },
                      );
                    } else {
                      return CategoryCard(category: categories[index]);
                    }
                  }),
                ),
              ),
            ),
            SizedBox(height: 16),
            PrimaryContainer(
              padding: EdgeInsets.zero,
              child: Column(
                children: [
                  Padding(
                    padding: EdgeInsets.all(16),
                    child: Row(
                      children: [
                        CustomHeaderText(
                          text: 'Cleaning Services',
                          fontSize: 18,
                        ),
                        const Spacer(),
                        CustomButton(
                          text: 'See All',
                          icon: AppAssets.kArrowForward,
                          isBorder: true,
                          onTap: () {},
                        ),
                      ],
                    ),
                  ),
                  SizedBox(
                    height: 195,
                    child: ListView.separated(
                      scrollDirection: Axis.horizontal,
                      padding: EdgeInsets.only(left: 16),
                      itemBuilder: (context, index) {
                        return HomeServicesCard(
                          service: cleaningServices[index],
                        );
                      },
                      separatorBuilder: (context, index) => SizedBox(width: 16),
                      itemCount: cleaningServices.length,
                    ),
                  ),
                  SizedBox(height: 16),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
