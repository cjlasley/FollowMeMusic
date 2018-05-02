//
//  FMNetwork.m
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/30/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import "FMNetwork.h"
#import <UIKit/UIKit.h>
#import <zlib.h>

static NSString * const BOUNDRY = @"0xKhTmLbOuNdArY";
static NSString * const FORM_FLE_INPUT = @"shent";

@implementation FMNetwork

- (id)initWithURL: (NSURL *)aServer filePath: (NSString *)aPath delegate: (id)aDelegate doneCallback: (SEL)aSelector errorCallback: (SEL)anotherSelector
{
    self = [super init];
    if (self) {
        
        serverURL                     = aServer;
        filePath                      = aPath;
        urlHandlingDelegate           = aDelegate;
        doneSendingMessageDestination = aSelector;
        errorMessageDestination       = anotherSelector;
        
        [self upload];
    }
    
    return self;
}

- (NSString *)filePath
{
    return filePath;
}

- (void)upload
{
    NSData *data = [NSData dataWithContentsOfFile:filePath];
    if (!data) {
        [self uploadDidSucceed:NO];
        return;
    }
    if ([data length] == 0) {
        [self uploadDidSucceed:YES];
        return;
    }
    
    //  NSData *compressedData = [self compress:data];
    //  ASSERT(compressedData && [compressedData length] != 0);
    //  if (!compressedData || [compressedData length] == 0) {
    //      [self uploadSucceeded:NO];
    //      return;
    //  }
    
    NSURLRequest *urlRequest = [self postRequestWithURL:serverURL boundry:BOUNDRY data:data];
    if (!urlRequest) {
        [self uploadDidSucceed:NO];
        return;
    }
    
    NSURLConnection * connection =
    [[NSURLConnection alloc] initWithRequest:urlRequest delegate:self];
    if (!connection) {
        [self uploadDidSucceed:NO];
    }
    
}

- (NSURLRequest *)postRequestWithURL: (NSURL *)theURL boundry: (NSString *)theBoundry data: (NSData *)theData
{
    NSMutableURLRequest *urlRequest = [NSMutableURLRequest requestWithURL:theURL];
    [urlRequest setHTTPMethod:@"POST"];
    
    NSMutableData *postData = [NSMutableData dataWithCapacity:[theData length] /*+ 512*/];
    
    [postData appendData:theData];
    
    [urlRequest setHTTPBody:postData];
    return urlRequest;
}

- (void)uploadDidSucceed:(BOOL)successStatus
{
    if (successStatus)
        [urlHandlingDelegate performSelector:doneSendingMessageDestination withObject:self];
    else
        [urlHandlingDelegate performSelector:errorMessageDestination withObject:self];
}

- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    printf("Done uploading to server!\n");
    
    [self uploadDidSucceed:YES];
}

- (void)connection:(NSURLConnection *)connection didFailWithError:(nonnull NSError *)error
{
    NSLog(@"%s: self:0x%p, connection error:%s\n",
          __func__, self, [[error description] UTF8String]);
    
    [self uploadDidSucceed:NO];
}

- (void)connection: (NSURLConnection *)connection didReceiveResponse:(NSURLResponse *)response
{
    printf("Got a response from the server!\n");
}

- (void)connection: (NSURLConnection *)connection didReceiveData:(NSData *)data
{
    printf("Got data from the server!\n");
    
    NSString *reply = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
    NSLog(@"%s: data: %s\n", __func__, [reply UTF8String]);
    
    if ([reply hasPrefix:@"YES"]) {
        printf("Yay!\n");
    }
}

- (void)dealloc
{
    serverURL = nil;
    filePath = nil;
    urlHandlingDelegate = nil;
    doneSendingMessageDestination = NULL;
    errorMessageDestination = NULL;
}

@end
