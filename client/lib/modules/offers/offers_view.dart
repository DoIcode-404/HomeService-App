import 'package:client/data/constants/constants.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/components/sub_category_grid_card.dart';
import 'package:client/modules/categories/components/sub_category_list_card.dart';
import 'package:client/modules/widgets/buttons/custom_icon_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class OffersView extends StatefulWidget {
  const OffersView({super.key});

  @override
  State<OffersView> createState() => _OffersViewState();
}

class _OffersViewState extends State<OffersView> {
  bool _isGridView = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 20),
            Row(
              children: [
                CustomHeaderText(text: 'Offers For You', fontSize: 18),
                const Spacer(),
                CustomIconButton(
                  onTap: () {
                    setState(() {
                      _isGridView = false;
                    });
                  },
                  isEnabled: _isGridView == false,
                  icon: AppAssets.kList,
                ),
                SizedBox(width: 8),
                CustomIconButton(
                  onTap: () {
                    setState(() {
                      _isGridView = true;
                    });
                  },
                  isEnabled: _isGridView == true,
                  icon: AppAssets.kGrid,
                ),
              ],
            ),
            SizedBox(height: 16),
            PrimaryContainer(
              child: AnimatedCrossFade(
                firstChild: ListView.separated(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemBuilder: (context, index) {
                    return SubCategoryListCard(service: allServices[index]);
                  },
                  separatorBuilder: (context, index) => const Divider(),
                  itemCount: 5,
                ),
                secondChild: GridView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    childAspectRatio: 148 / 237,
                    mainAxisSpacing: 10,
                    crossAxisSpacing: 10,
                  ),
                  itemCount: 6,
                  itemBuilder: (context, index) {
                    return SubCategoryGridCard(service: allServices[index]);
                  },
                ),
                crossFadeState:
                    _isGridView
                        ? CrossFadeState.showSecond
                        : CrossFadeState.showFirst,
                duration: const Duration(milliseconds: 500),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
