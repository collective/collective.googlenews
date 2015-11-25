Changelog
=========

2.0a1 (unreleased)
-------------------

- Keywords mapping feature was removed as the values on the ``<keywords>`` tag of Google News Sitemaps may be drawn from, but are not limited to, the list of existing Google News keywords (closes `#14`_).
  [hvelarde]

- Add support for Editors' Picks feeds (closes `#9`_).
  [rodfersou, hvelarde]

- Get rid of the '.html' on the ids (closes `#8`_).
  [hvelarde]

- Update package dependencies.
  [hvelarde]

- Drop support for Plone 4.0, Plone 4.1, Plone 4.2 and Python 2.6.
  [hvelarde]

- Updated Spanish translation. [macagua]

- Updated i18n support. [macagua]


1.0rc3 (2013-01-24)
-------------------

- Add keyword mapping support.
- Update french translations


1.0rc2 (2012-07-24)
-------------------

- Replaced the UserFriendlyTypes vocabulary in favor of
  ReallyUserFriendlyTypes. [frapell]

- Do not run uninstall profile on reinstall. [hvelarde]

- Control panel widget was replaced; we use now Choice instead of ASCIILine
  (fixes `#3`_). [hvelarde]

- Updated Spanish and Brazilian Portuguese translations. [hvelarde]

- Updated package documentation. [hvelarde]


1.0rc1 (2012-05-11)
-------------------

- Tested Plone 4.2 compatibility. [hvelarde]

- Added support for Dexterity content types (fixes `#2`_). [flecox]

- Added Spanish and Brazilian Portuguese translations. [hvelarde]

- Added some real tests to fix some stuff. [hvelarde]

- Updated package distribution files. [hvelarde]


1.0b2 (2011-04-11)
------------------

- Check random digit doesn't starts with 199 or 200.


1.0b1 (2011-04-08)
------------------

- Initial release.

.. _`#2`: https://github.com/collective/collective.googlenews/issues/2
.. _`#3`: https://github.com/collective/collective.googlenews/issues/3
.. _`#8`: https://github.com/collective/collective.googlenews/issues/8
.. _`#9`: https://github.com/collective/collective.googlenews/issues/9
.. _`#14`: https://github.com/collective/collective.googlenews/issues/14
