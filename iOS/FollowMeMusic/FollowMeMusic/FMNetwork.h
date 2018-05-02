//
//  FMNetwork.h
//  FollowMeMusic
//
//  Created by Collin Lasley on 4/30/18.
//  Copyright © 2018 clasley. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface FMNetwork : NSObject<NSURLSessionDelegate>
{
    NSURL *serverURL;
    NSString *filePath;
    id urlHandlingDelegate;
    SEL doneSendingMessageDestination;
    SEL errorMessageDestination;
}

- (id)initWithURL: (NSURL *)aServer filePath: (NSString *)aPath delegate: (id)aDelegate doneCallback: (SEL)aSelector errorCallback: (SEL)anotherSelector;

- (NSString *)filePath;

- (void)upload;

- (NSURLRequest *)postRequestWithURL: (NSURL *)theURL boundry: (NSString *)theBoundry data: (NSData *)theData;

- (NSData *)compressData:(NSData *)data;

- (void)uploadDidSucceed:(BOOL)successStatus;

- (void)connectionDidFinishLoading:(NSURLConnection *)connection;

- (void)dealloc;

@end
