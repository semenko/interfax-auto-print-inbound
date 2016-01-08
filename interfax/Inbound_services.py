################################################## 
# Inbound_services.py 
# generated by ZSI.generate.wsdl2python
##################################################


from Inbound_services_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
import ZSI

# Locator
class InboundLocator:
    InboundSoap_address = "https://ws.interfax.net/inbound.asmx"
    def getInboundSoapAddress(self):
        return InboundLocator.InboundSoap_address
    def getInboundSoap(self, url=None, **kw):
        return InboundSoapSOAP(url or InboundLocator.InboundSoap_address, **kw)

# Methods
class InboundSoapSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: ResendInboundToEmail
    def ResendInboundToEmail(self, request):
        if isinstance(request, ResendInboundToEmailSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/ResendInboundToEmail", **kw)
        # no output wsaction
        response = self.binding.Receive(ResendInboundToEmailSoapOut.typecode)
        return response

    # op: GetInboundLogEmails
    def GetInboundLogEmails(self, request):
        if isinstance(request, GetInboundLogEmailsSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/GetInboundLogEmails", **kw)
        # no output wsaction
        response = self.binding.Receive(GetInboundLogEmailsSoapOut.typecode)
        return response

    # op: GetList
    def GetList(self, request):
        if isinstance(request, GetListSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/GetList", **kw)
        # no output wsaction
        response = self.binding.Receive(GetListSoapOut.typecode)
        return response

    # op: GetList2
    def GetList2(self, request):
        if isinstance(request, GetList2SoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/GetList2", **kw)
        # no output wsaction
        response = self.binding.Receive(GetList2SoapOut.typecode)
        return response

    # op: GetImageChunkEx2
    def GetImageChunkEx2(self, request):
        if isinstance(request, GetImageChunkEx2SoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/GetImageChunkEx2", **kw)
        # no output wsaction
        response = self.binding.Receive(GetImageChunkEx2SoapOut.typecode)
        return response

    # op: GetImageChunk
    def GetImageChunk(self, request):
        if isinstance(request, GetImageChunkSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/GetImageChunk", **kw)
        # no output wsaction
        response = self.binding.Receive(GetImageChunkSoapOut.typecode)
        return response

    # op: MarkMessage
    def MarkMessage(self, request):
        if isinstance(request, MarkMessageSoapIn) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        kw = {}
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://www.interfax.net/MarkMessage", **kw)
        # no output wsaction
        response = self.binding.Receive(MarkMessageSoapOut.typecode)
        return response

ResendInboundToEmailSoapIn = ns0.ResendInboundToEmail_Dec().pyclass

ResendInboundToEmailSoapOut = ns0.ResendInboundToEmailResponse_Dec().pyclass

GetInboundLogEmailsSoapIn = ns0.GetInboundLogEmails_Dec().pyclass

GetInboundLogEmailsSoapOut = ns0.GetInboundLogEmailsResponse_Dec().pyclass

GetListSoapIn = ns0.GetList_Dec().pyclass

GetListSoapOut = ns0.GetListResponse_Dec().pyclass

GetList2SoapIn = ns0.GetList2_Dec().pyclass

GetList2SoapOut = ns0.GetList2Response_Dec().pyclass

GetImageChunkEx2SoapIn = ns0.GetImageChunkEx2_Dec().pyclass

GetImageChunkEx2SoapOut = ns0.GetImageChunkEx2Response_Dec().pyclass

GetImageChunkSoapIn = ns0.GetImageChunk_Dec().pyclass

GetImageChunkSoapOut = ns0.GetImageChunkResponse_Dec().pyclass

MarkMessageSoapIn = ns0.MarkMessage_Dec().pyclass

MarkMessageSoapOut = ns0.MarkMessageResponse_Dec().pyclass