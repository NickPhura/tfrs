package specs

import pages.HomePage
import pages.CreditTransactionsPage
import pages.CompanyDetailsPage
import pages.ExternalLinkPage
import pages.ContactUsPage

import spock.lang.Timeout
import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Unroll

@Timeout(60)
@Title('Flow Tests')
@Narrative('''
As a developer, I want to ensure all page links work, have the correct text, and direct to the correct page.
''')
class FlowSpecs extends LoggedInSpec {

  void setup() {
    logInAsSendingFuelSupplier()
  }

  @Unroll
  void 'Navigate Page from: HomePage, click header Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
    when: 'I click on the header link with label: #TextSelector.text'
      headerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector                    || AssertPage
      // TODO pdfs in headless mode dont work (works in headful mode)
      // [ text:'Fuel Suppliers' ]       || new ExternalLinkPage('013\\.pdf', 'www2\\.gov\\.bc\\.ca.*013\\.pdf')
      [ text:'Company Details' ]      || CompanyDetailsPage
      // TODO pdfs in headless mode dont work (works in headful mode)
      // [ text:'Credit Market Report' ] || new ExternalLinkPage('017\\.pdf', 'www2\\.gov\\.bc\\.ca.*017\\.pdf')
      [ text:'Credit Transactions' ]  || CreditTransactionsPage
  }

  @Unroll
  void 'Navigate Page from: HomePage, click footer Link: #TextSelector, Assert Page: #AssertPage'() {
    given: 'I start on the HomePage'
    when: 'I click on the footer link with label: #TextSelector.text'
      footerModule.clickMenuItem(TextSelector)
    then: 'I arrive on the #AssertPage.getSimpleName()'
      at AssertPage
    where:
      TextSelector               || AssertPage
      [ text:'Home' ]            || HomePage
      [ text:'About this site' ] || HomePage
      [ text:'Disclaimer' ]      || new ExternalLinkPage('Disclaimer - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*disclaimer')
      [ text:'Privacy' ]         || new ExternalLinkPage('B\\.C\\. Government Website Privacy Statement - Province of \
                                                          British Columbia', 'www2\\.gov\\.bc\\.ca.*privacy')
      [ text:'Accessibility' ]   || new ExternalLinkPage('Web Accessibility - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*accessibility')
      [ text:'Copyright' ]       || new ExternalLinkPage('Copyright - Province of British Columbia',
                                                         'www2\\.gov\\.bc\\.ca.*copyright')
      [ text:'Contact Us' ]      || ContactUsPage
  }
}
