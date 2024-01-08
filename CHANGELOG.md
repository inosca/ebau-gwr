# Changelog

## v0.6.3 (2024-01-08)

### Fix
* **deps:** Downgrade python-semantic-release to v7.33.3 ([`803b619`](https://github.com/inosca/ebau-gwr/commit/803b619654e9b858d173e7200e9b87f40861289e))
* **deps:** Update dependencies ([`0bd1823`](https://github.com/inosca/ebau-gwr/commit/0bd18236164af1747a1589809028de1f9786e1bb))

## v0.6.2 (2023-05-12)

### Fix
* **deps:** Update dependencies ([`e259b36`](https://github.com/inosca/ebau-gwr/commit/e259b362e87931d2258767c716ee4638eb3be351))

## v0.6.1 (2022-09-21)

### Fix
* **linker:** Allow "in" lookup for gwr-link eproid filter ([`bcaa1d1`](https://github.com/inosca/ebau-gwr/commit/bcaa1d1b58c285019db2bff466c23c2902a6e41d))

## v0.6.0 (2022-09-02)

### Feature
* **hous_stat_creds:** Creds are identified by user and x-camac-group ([`7894081`](https://github.com/inosca/ebau-gwr/commit/789408155bcf92450efac7bf90a42dfe4bf070f2))

### Fix
* **docker:** Run server with poetry so deps are found ([`cbbbd71`](https://github.com/inosca/ebau-gwr/commit/cbbbd717f670ee9b2ee6ec3af86704bc340ad670))

## v0.5.2 (2022-06-20)

### Fix
* **deps:** Update dependencies ([`be92236`](https://github.com/inosca/ebau-gwr/commit/be92236798245053c44d51cac5ec454f1d2be9fb))

## v0.5.1 (2022-04-21)

### Fix
* **deps:** Update dependencies ([`fc7415e`](https://github.com/inosca/ebau-gwr/commit/fc7415e1e1db9445652d3da22d9fe4cb9a03fa20))

## v0.5.0 (2022-03-03)

### Breaking
* This commit updates django to version 3.2 which is a new major version. If this package is consumed as django app, the host app needs to update django as well: ([`4adaec2`](https://github.com/inosca/ebau-gwr/commit/4adaec29c7475b99f411d81de2947f8b9a2c0794))

### Documentation
* **readme:** Fix build status badge ([`66d222a`](https://github.com/inosca/ebau-gwr/commit/66d222acf85df447f5fd1af3c102751a3b5f62ec))

## v0.4.1 (2021-10-27)

### Fix
* Gwr base uri config settings ([`9f215b9`](https://github.com/inosca/ebau-gwr/commit/9f215b96dd087524548d60cd65f5b2fa17530ed3))
* License identifier ([`c01f050`](https://github.com/inosca/ebau-gwr/commit/c01f0509a2dd16ea3a34eef5dd9dc3625f99a8f4))

## v0.4.0 (2021-07-08)

### Feature
* Allow removal of housing stat credentials ([`20c1f09`](https://github.com/inosca/ebau-gwr/commit/20c1f09e0d9871236cd6950b89e55e10fb0bfe2c))
# v0.3.0 (2021-05-06)

### Feature
* **token_proxy:** Add municipality as a field ([`a08e989`](https://github.com/inosca/ebau-gwr/commit/a08e989864063e17803dc2a17da2ce6b58aa1040))

## v0.2.0 (2021-04-14)

### Feature
* Introduce command to generate fernet key ([`949ef82`](https://github.com/inosca/ebau-gwr/commit/949ef82fe407680b2e961d1564aba5ac956ab50b))
* Introduce token_proxy app ([`65f4323`](https://github.com/inosca/ebau-gwr/commit/65f43238b5a27cc55d7b087565b179a53aa4f2c4))

### Fix
* Define default ordering on GWRLink model ([`4a1fae3`](https://github.com/inosca/ebau-gwr/commit/4a1fae352ce4d3a269e111ddeb43a0d055926d89))

### Documentation
* **readme:** Document correct env var name for wsk_id ([`39140c9`](https://github.com/inosca/ebau-gwr/commit/39140c97feb94cd8bcdff053b82c6d0e2790386c))

## v0.1.0 (2021-02-22)

### Feature
* Integrate django-generic-api-permissions ([`eea32d9`](https://github.com/czosel/ebau-gwr/commit/eea32d9b74416fa75d4a9e667993162b110bba1a))
* **linker:** Introduce linker app ([`94afc2a`](https://github.com/czosel/ebau-gwr/commit/94afc2a1dd11c99f7a73bac0e03327a16637d088))
* Introduce /construction_project retrieve view ([`7dc0de9`](https://github.com/czosel/ebau-gwr/commit/7dc0de97cc910e3e98e73fbc3bfe40a11e73a646))
* Introduce /search endpoint ([`01aaf20`](https://github.com/czosel/ebau-gwr/commit/01aaf202b78f2c69dd542cd15c7e001ca86df0ee))
* Add xml schema and formatters.py ([`9ee8a76`](https://github.com/czosel/ebau-gwr/commit/9ee8a760b31ec4cc17ea8284699f4801e8e7ec24))

### Fix
* Rename url path to match jsonapi spec ([`e637a99`](https://github.com/czosel/ebau-gwr/commit/e637a99167315381de70814860e3ad2805d82117))
* Install_requires ([`285c34d`](https://github.com/czosel/ebau-gwr/commit/285c34df2ba88ea680039212bf89d0acbe1e0a2e))
* Release workflow ([`aca6bdb`](https://github.com/czosel/ebau-gwr/commit/aca6bdb4ba559213bb6363a816b333168a78f6c6))
* Pypi release script ([`fe5e46b`](https://github.com/czosel/ebau-gwr/commit/fe5e46b655f2008801f7035ac5a2f41efac1f9f2))
* Drop pyxb, add dependencies to setup.cfg ([`35b98dc`](https://github.com/czosel/ebau-gwr/commit/35b98dc2c078910ca9642386a27fe6dabf16500b))
* Drop core app ([`1c7c73a`](https://github.com/czosel/ebau-gwr/commit/1c7c73a066e897742507fa00b099c198df8d33f0))

## v0.0.a3 (2021-02-16)

Initial release
