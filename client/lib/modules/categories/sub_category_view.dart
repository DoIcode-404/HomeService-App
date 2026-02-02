import 'package:client/data/constants/constants.dart';
import 'package:client/model/category_model.dart';
import 'package:client/model/service_model.dart';
import 'package:client/modules/categories/components/sub_category_grid_card.dart';
import 'package:client/modules/categories/components/sub_category_list_card.dart';
import 'package:client/modules/home/components/search_field.dart';
import 'package:client/modules/widgets/buttons/custom_icon_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class SubCategoryView extends StatefulWidget {
  final CategoryModel category;

  const SubCategoryView({required this.category, super.key});

  @override
  State<SubCategoryView> createState() => _SubCategoryViewState();
}

class _SubCategoryViewState extends State<SubCategoryView> {
  final _searchController = TextEditingController();
  bool _isGridView = false;

  List<ServicesModel> subCategoriesList = [];

  @override
  void initState() {
    super.initState();
    filterServicesByCategory(widget.category);
  }

  void filterServicesByCategory(CategoryModel category) {
    setState(() {
      subCategoriesList =
          allServices.where((service) => service.category == category).toList();
    });
  }

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
            PrimaryContainer(
              child: SearchField(
                controller: _searchController,
                onSearchPress: () {},
              ),
            ),
            SizedBox(height: 16),
            Row(
              children: [
                CustomHeaderText(text: widget.category.name, fontSize: 18),
                const Spacer(),
                CustomIconButton(
                  onTap: () {
                    setState(() {
                      _isGridView = false;
                    });
                  },
                  isEnabled: !_isGridView,
                  icon: AppAssets.kList,
                ),
                SizedBox(width: 8),
                CustomIconButton(
                  onTap: () {
                    setState(() {
                      _isGridView = true;
                    });
                  },
                  isEnabled: _isGridView,
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
                    final service = subCategoriesList[index];
                    return SubCategoryListCard(service: service);
                  },
                  separatorBuilder: (context, index) => const Divider(),
                  itemCount: subCategoriesList.length,
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
                  itemCount: subCategoriesList.length,
                  itemBuilder: (context, index) {
                    final service = subCategoriesList[index];
                    return SubCategoryGridCard(service: service);
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
